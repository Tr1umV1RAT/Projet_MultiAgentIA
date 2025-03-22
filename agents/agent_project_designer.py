from agents.base_agent import BaseAgent
from roles.project_designer import ProjectDesignerRole
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message


class AgentProjectDesigner(BaseAgent):
    def __init__(self, nom="AgentProjectDesigner", role=None, memoire_persistante=None):
        role = role or ProjectDesignerRole()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication()
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="project_designer_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante du Project Designer"
        )
        self.db_skill = DBManagementSkill(db_name="project_designer_memory.db", schema=Config.MEMORY_TABLE_SCHEMA)
        skills = [self.memoire_court_terme, self.communication, self.db_skill]
        if memoire_persistante:
            skills.append(memoire_persistante)

        super().__init__(name=nom, role=role, skills=skills)

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide pour un Project Designer.",
                meta={"error": "invalid_input"}
            )

        prompt = f"""
Tu es un Project Designer senior. Voici la commande initiale :

{message.contenu}

Ta mission est de produire :
1. Une clarification du besoin
2. Une découpe du projet en modules ou fichiers
3. Une structure de fichiers suggérée
4. Des recommandations pour l'organisation de travail de l'équipe

Sois synthétique mais complet. N'invente pas de fonctionnalités non demandées.
"""

        msg_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "analyse_initiale"}
        )

        result = self.reasoning.reflechir(msg_llm)

        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": "analyse_projet"}
        ))

        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Analyse initiale du projet :\n\n{result.contenu}",
            dialogue=True
        )
