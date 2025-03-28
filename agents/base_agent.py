import os
from tools.llm_interface import LLMInterface
from skills.communication import Communication
from skills.communication.messages import Message
from skills.memory.memory_skill import MemorySkill

class BaseAgent:
    def __init__(self, name, role=None, skills=None, verbose=False, llm=None, base_path="agent_memories"):
        self.name = name
        self.role = role
        self.verbose = verbose
        self.llm = llm if llm else LLMInterface(agent=self, verbose=verbose)

        # Crée un dossier mémoire dédié spécifiquement à cet agent
        agent_memory_path = os.path.join(base_path, self.name)
        os.makedirs(agent_memory_path, exist_ok=True)

        self.memory_skill = MemorySkill(name, self.llm, base_path=agent_memory_path, verbose=False)
        self.memory = self.memory_skill.manager
        self.retriever = self.memory_skill.retriever

        self.communication = Communication(verbose=False)

        self.skills = skills if skills else []
        self.skills.append(self.memory_skill)

    def receive_message(self, message):
        self.memory.store_message(message)
        return self.process_message(message)

    def process_message(self, message):
        context = self.retriever.retrieve_relevant_memory(message)
        prompt = context + "\n" + message.contenu

        if self.role:
            prompt = self.role.get_prompt(prompt)

        response_content = self.llm.query(prompt)

        response_message = Message(
            origine=self.name,
            destinataire=message.origine,
            contenu=response_content,
            conversation_id=message.conversation_id
        )

        self.communication.send(response_message)
        self.memory.store_message(response_message)

        return response_message

# Fonction CLI permettant des échanges persistants
def cli_chat():
    import sys
    agent_name = "AgentCLI"
    agent = BaseAgent(name=agent_name)

    print(f"Discussion avec {agent_name} (tape 'quit' pour quitter) :")

    conversation_id = None

    while True:
        user_input = input("Vous: ")
        if user_input.lower() == 'quit':
            break

        user_message = Message(
            origine="utilisateur",
            destinataire=agent.name,
            contenu=user_input,
            conversation_id=conversation_id  # même id pour toute la conversation
        )

        response = agent.receive_message(user_message)

        # garder le même id pour poursuivre la conversation
        conversation_id = response.conversation_id  

        print(f"{agent.name}: {response.contenu}")

if __name__ == "__main__":
    cli_chat()
