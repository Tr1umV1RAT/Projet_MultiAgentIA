from agents.base_agent import BaseAgent
from roles.project_manager import ProjectManagerRole
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message
import re
import uuid

class AgentProjectManager(BaseAgent):
    def __init__(self, nom="AgentProjectManager", role=None, memoire_persistante=None):
        role = role or ProjectManagerRole()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication()
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="project_manager_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante de l'agent project_manager"
        )

        self.db_skill = DBManagementSkill(db_name="project_manager_memory.db", schema=Config.MEMORY_TABLE_SCHEMA)
        skills = [self.memoire_court_terme, self.communication, self.db_skill]
        if memoire_persistante:
            skills.append(memoire_persistante)

        super().__init__(name=nom, role=role, skills=skills)

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide reçu. Veuillez transmettre un résumé ou un statut de tâche.",
                meta={"error": "invalid_input"}
            )

        prompt = f"""
Tu es le chef de projet. Voici le dernier message reçu :

{message.contenu}

Ta tâche est de faire un point sur la situation du projet, analyser les étapes restantes, et proposer la suite à donner.
"""

        msg_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "synthese_avancement"}
        )

        result = self.reasoning.reflechir(msg_llm)

        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": "synthese", "source": "ProjectManager"}
        ))

        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Synthèse de l’avancement :\n\n{result.contenu}",
            dialogue=True
        )