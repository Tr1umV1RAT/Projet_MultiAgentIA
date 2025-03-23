# agents/agent_project_manager.py
import re
from agents.base_agent import BaseAgent
from roles.project_manager import ProjectManagerRole
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message

class AgentProjectManager(BaseAgent):
    def __init__(self, nom="AgentProjectManager", role=None, memoire_persistante=None):
        role = role or ProjectManagerRole()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication()
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="project_manager_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante de l'agent project manager"
        )
        self.db_skill = DBManagementSkill(
            db_name="project_manager_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            connexion=self.memoire_persistante.connexion
        )
        skills = [self.memoire_court_terme, self.communication, self.db_skill, self.memoire_persistante]
        super().__init__(name=nom, role=role, skills=skills)
    
    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide reçu. Veuillez transmettre un résumé ou un statut de tâche.",
                meta={"error": "invalid_input"},
                dialogue=True
            )
        # Différencier l'analyse du projet de la synthèse générale
        if message.meta.get("type_message") == "analyse_projet":
            prompt = f"""
Tu es le chef de projet. En te basant sur l'analyse suivante du Project Designer, définis les priorités pour le prochain cycle de développement. Identifie les tâches essentielles, les points bloquants et propose des recommandations concrètes.

Analyse reçue :
{message.contenu}

Réponds par une liste ordonnée des priorités avec des recommandations pour chaque tâche.
"""
            instruction = "priorisation"
        else:
            prompt = f"""
Tu es le chef de projet. Voici le dernier message reçu :

{message.contenu}

Ta tâche est de faire un point sur la situation du projet, d'analyser les étapes restantes et de proposer la suite à donner.
"""
            instruction = "synthese_avancement"
        
        msg_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": instruction}
        )
        result = self.reasoning.reflechir(msg_llm)
        message_type = "priorisation" if instruction == "priorisation" else "synthese"
        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": message_type, "source": "ProjectManager"},
            dialogue=False
        ))
        if instruction == "priorisation":
            retour = f"Priorités définies :\n\n{result.contenu}"
        else:
            retour = f"Synthèse de l’avancement :\n\n{result.contenu}"
        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=retour,
            meta={},
            dialogue=True
        )
