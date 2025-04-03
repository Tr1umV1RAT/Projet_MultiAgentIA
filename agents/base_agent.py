import os
from datetime import datetime
from typing import Optional, List

from tools.llm_interface import LLMInterface
from skills.communication import Communication
from skills.communication.messages import Message
from skills.communication.prompt_builder import PromptBuilder
from skills.memory.memory_skill import MemorySkill
from skills.skill_manager import SkillManager
from config import Config

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

        # Initialisation des dossiers mémoire
        agent_memory_path = os.path.join(base_path, self.name)
        os.makedirs(agent_memory_path, exist_ok=True)

        # Initialisation unique du Skill de Mémoire
        self.memory_skill = MemorySkill(
            name=self.name, 
            llm=self.llm, 
            base_path=agent_memory_path, 
            verbose=verbose
        )
        self.memory = self.memory_skill.manager
        self.retriever = self.memory_skill.retriever

        # Initialisation de la communication
        self.communication = Communication(verbose=Config.verbose_communication)

        # Initialisation et intégration complète du SkillManager
        self.skill_manager = SkillManager(self)
        self.skills = skills if skills else []

        # Ajout du skill de mémoire par défaut
        self.skill_manager.add_skill("memory", self.memory_skill)
        self.skill_manager.activate_skill("memory")

        # Ajout des autres skills fournis à l'initialisation
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
        # Vérifie les actions définies dans les métadonnées et délègue au SkillManager
        response = self.skill_manager.handle_message(message)
        if response:
            self.communication.send(response)
            self.memory.store_message(response)
            return response

        # Si aucun skill n'est déclenché explicitement et que c'est une commande spéciale, ne rien faire
        if message.contenu.lower() in ["activate", "execute", "deactivate"]:
            if self.verbose:
                print(f"[{self.name}] Commande spéciale '{message.contenu}' reçue, pas de réponse générée.")
            return None

        # Traitement standard si aucune skill n'est déclenchée explicitement
        return self.process_message(message)

    def process_message(self, message: Message):
        context = self.retriever.build_context(message)

        if self.role:
            prompt = PromptBuilder.build(role=self.role, **context)
        else:
            prompt = ""
            if context.get("memory"):
                prompt += f"🧠 CONTEXTE :\n{context['memory']}\n\n"
            prompt += f"🎯 INSTRUCTION :\n{context['instruction']}"

        response_content = self.llm.query(prompt)

        response_message = Message(
            origine=self.name,
            destinataire=message.origine,
            contenu=response_content,
            conversation_id=message.conversation_id,
            metadata={"context_used": context}
        )

        self.communication.send(response_message)
        self.memory.store_message(response_message)

        return response_message


def cli_chat():
    agent = BaseAgent(verbose=True)

    conversation_id = None

    while True:
        user_input = input("Vous (ou 'quit', 'activate', 'execute', 'deactivate'): ")
        if user_input.lower() == 'quit':
            break

        # Test explicite pour l'activation/désactivation des skills
        if user_input in ["activate", "execute", "deactivate"]:
            metadata = {}
            if user_input == "activate":
                metadata = {"activate_skill": "memory"}
            elif user_input == "execute":
                metadata = {"skill": "memory"}
            elif user_input == "deactivate":
                metadata = {"deactivate_skill": "memory"}

            message = Message(
                origine="utilisateur",
                destinataire=agent.name,
                contenu=user_input,
                metadata=metadata
            )
        else:
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
