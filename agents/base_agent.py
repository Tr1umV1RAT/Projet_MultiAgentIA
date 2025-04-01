import os
from datetime import datetime
from typing import Optional

from tools.llm_interface import LLMInterface
from skills.communication import Communication
from skills.communication.messages import Message
from skills.communication.prompt_builder import PromptBuilder
from skills.memory.memory_skill import MemorySkill

class BaseAgent:
    def __init__(self, name=None, role=None, skills=None, verbose=False, llm=None, base_path="agent_memories"):
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"Agent_{timestamp}"

        self.name = name
        self.role = role
        self.verbose = verbose
        self.llm = llm if llm else LLMInterface(agent=self, verbose=verbose)

        agent_memory_path = os.path.join(base_path, self.name)
        os.makedirs(agent_memory_path, exist_ok=True)

        self.memory_skill = MemorySkill(name, self.llm, base_path=agent_memory_path, verbose=verbose)
        self.memory = self.memory_skill.manager
        self.retriever = self.memory_skill.retriever

        self.communication = Communication(verbose=verbose)

        self.skills = skills if skills else []
        self.skills.append(self.memory_skill)

    @classmethod
    def from_config(cls, config: dict, verbose=False):
        name = config.get("name")
        # TODO : charger d'autres infos comme le role, les skills, etc.
        return cls(name=name, verbose=verbose)

    def get_skill_by_name(self, name: str):
        for skill in self.skills:
            if hasattr(skill, "name") and skill.name == name:
                return skill
        return None

    def receive_message(self, message):
        if action := getattr(message, "action", None):
            if self.verbose:
                print(f"[{self.name}] Action '{action}' détectée — délégation à la skill correspondante.")
            skill = self.get_skill_by_name(action)
            if skill:
                return skill.run(message)
            elif self.verbose:
                print(f"[{self.name}] Aucun skill nommé '{action}' trouvé dans l'agent.")
            return None
        return self.process_message(message)

    def process_message(self, message):
        memory_summary = self.retriever.get_memory_summary(message)

        if self.role:
            prompt = PromptBuilder.build(
                role=self.role,
                instruction=message.contenu,
                memory=memory_summary
            )
        else:
            prompt = ""
            if memory_summary:
                prompt += f"🧠 CONTEXTE :\n{memory_summary}\n\n"
            prompt += f"🎯 INSTRUCTION :\n{message.contenu}"

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

def cli_chat():
    import sys
    agent = BaseAgent(verbose=True)

    print(f"Discussion avec {agent.name} (tape 'quit' pour quitter) :")

    conversation_id = None

    while True:
        user_input = input("Vous: ")
        if user_input.lower() == 'quit':
            break

        user_message = Message(
            origine="utilisateur",
            destinataire=agent.name,
            contenu=user_input,
            conversation_id=conversation_id
        )

        response = agent.receive_message(user_message)
        if response:
            conversation_id = response.conversation_id
            print(f"{agent.name}: {response.contenu}")
        else:
            print(f"{agent.name}: (aucune réponse)")


if __name__ == "__main__":
    cli_chat()
