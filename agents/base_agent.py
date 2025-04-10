import os
from datetime import datetime
from typing import Optional, List

from tools.llm_interface import LLMInterface
from skills.communication import Communication
from skills.communication.messages import Message
from skills.communication.prompt_builder import PromptBuilder
from skills.skill_manager import SkillManager
from config import Config

from skills.memory.memory_pipeline import MemoryPipeline  # nouvelle base de mémoire

class BaseAgent:
    def __init__(
        self, 
        name: Optional[str] = None, 
        role: Optional[object] = None, 
        skills: Optional[List[object]] = None, 
        verbose: bool = Config.verbose,
        llm: Optional[LLMInterface] = None,
        base_path: str = "agent_memories"
    ):
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"Agent_{timestamp}"

        self.name = name
        self.role = role
        self.verbose = verbose

        # Initialisation de l'interface LLM
        self.llm = llm if llm else LLMInterface(agent=self, verbose=verbose)

        # Initialisation du pipeline de mémoire
        agent_memory_path = os.path.join(base_path, self.name)
        os.makedirs(agent_memory_path, exist_ok=True)
        self.memory_pipeline = MemoryPipeline(agent_name=self.name, role=self.role, llm=self.llm, base_path=base_path)


        # Initialisation de la communication
        self.communication = Communication(verbose=Config.verbose_communication)

        # Initialisation et intégration du SkillManager
        self.skill_manager = SkillManager(self)
        self.skills = skills if skills else []

        for skill in self.skills:
            self.skill_manager.add_skill(skill.name, skill)
            self.skill_manager.activate_skill(skill.name)

    @classmethod
    def from_config(cls, config: dict, verbose=Config.verbose):
        name = config.get("name")
        role = config.get("role")
        skills = config.get("skills", [])
        llm = config.get("llm")

        return cls(name=name, role=role, skills=skills, verbose=verbose, llm=llm)

    def receive_message(self, message: Message):
        # Enregistrement systématique en mémoire
        self.memory_pipeline.store_message(message)

        # Vérifie les actions définies dans les métadonnées et délègue au SkillManager
        response = self.skill_manager.handle_message(message)
        if response:
            self.communication.send(response)
            self.memory_pipeline.store_message(response)
            return response

        # Si commande spéciale sans traitement
        if message.contenu.lower() in ["activate", "execute", "deactivate"]:
            if self.verbose:
                print(f"[{self.name}] Commande spéciale '{message.contenu}' reçue, pas de réponse générée.")
            return None

        return self.process_message(message)

    def process_message(self, message: Message):
        context = self.memory_pipeline.get_context(message)

        prompt = f"{context}\n\n🎯 INSTRUCTION :\n{message.contenu}"
        response_content = self.llm.query(prompt)

        response_message = Message(
            origine=self.name,
            destinataire=message.origine,
            contenu=response_content,
            conversation_id=message.conversation_id,
            metadata={"context_used": context}
        )

        self.communication.send(response_message)
        self.memory_pipeline.store_message(response_message)

        return response_message

def cli_chat():
    agent = BaseAgent(verbose=True)

    conversation_id = None

    while True:
        user_input = input("Vous (ou 'quit') : ")
        if user_input.lower() == 'quit':
            break

        message = Message(
            origine="utilisateur",
            destinataire=agent.name,
            contenu=user_input,
            conversation_id=conversation_id
        )

        response = agent.receive_message(message)

        if response:
            conversation_id = response.conversation_id
            print(f"{agent.name}: {response.contenu}")
        else:
            print(f"{agent.name}: (aucune réponse)")

if __name__ == "__main__":
    cli_chat()
