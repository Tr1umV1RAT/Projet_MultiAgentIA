from agents.base_agent import BaseAgent
from skills.coder_skill import CoderSkill
from roles.codeur import Codeur
from tools.llm_interface import LLMInterface
from skills.communication.messages import Message

class AgentCodeur(BaseAgent):
    def __init__(self, name, verbose=False):
        role = Codeur()
        llm = LLMInterface(verbose=verbose)
        
        super().__init__(name, role=role, verbose=verbose, llm=llm)

        # Ajouter spécifiquement le skill Coder à cet agent
        self.coder_skill = CoderSkill(llm, verbose=verbose)
        self.skills.append(self.coder_skill)

    def process_message(self, message: Message):
        # Utiliser explicitement le skill de codage
        code_result = self.coder_skill.generate_code(message.contenu)

        response_message = Message(
            origine=self.name,
            destinataire=message.origine,
            contenu=code_result,
            conversation_id=message.conversation_id
        )

        self.communication.send(response_message)
        self.memory.store_message(response_message)

        if self.verbose:
            print(f"[{self.name}] Code généré :\n{code_result}")

        return response_message

if __name__ == "__main__":
    import sys
    prompt_cli = sys.argv[1] if len(sys.argv) > 1 else "Ecris une fonction Python qui additionne deux nombres"
    
    agent = AgentCodeur(name="AgentCodeurCLI", verbose=True)

    message_cli = Message(
        origine="utilisateur",
        destinataire=agent.name,
        contenu=prompt_cli
    )

    response = agent.receive_message(message_cli)
    print(f"Code généré par {agent.name} :\n{response.contenu}")
