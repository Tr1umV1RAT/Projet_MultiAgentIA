# agents/agent_reviewer.py

from agents.base_agent import BaseAgent
from roles.reviewer import ReviewerRole
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message

class AgentReviewer(BaseAgent):
    def __init__(self, nom="AgentReviewer", role=None, memoire_persistante=None, verbose=False):
        role = role or ReviewerRole()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication(verbose=verbose)
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="reviewer_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante de l'agent reviewer"
        )
        self.db_skill = DBManagementSkill(db_name="reviewer_memory.db", schema=Config.MEMORY_TABLE_SCHEMA)
        skills = [self.memoire_court_terme, self.communication, self.db_skill, self.memoire_persistante]
        super().__init__(name=nom, role=role, skills=skills, verbose=verbose)
        self.reasoning = Reasoning(self)
        if self.verbose:
            print(f"[{self.name} INIT] Agent Reviewer initialisé en mode verbeux.")

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide. Veuillez soumettre un contenu à relire.",
                meta={"error": "invalid_message"},
                dialogue=True
            )
        prompt = f"""
Tu es un reviewer professionnel. Voici les critères d'évaluation :

1. Clarté du code ou du contenu fourni.
2. Respect des consignes.
3. Qualité de la documentation (docstrings, nommage clair, etc.).
4. Cohérence fonctionnelle.
5. Améliorations possibles.

Travail à analyser :
{message.contenu}
"""
        msg_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "review_request", "original_task": message.meta.get("task", "")}
        )
        result = self.reasoning.reflechir(msg_llm)
        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": "review", "review_of": message.meta.get("filename", "unknown")},
            dialogue=False
        ))
        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Voici mon avis sur le fichier {message.meta.get('filename', 'inconnu')} :\n\n{result.contenu}",
            meta={},
            dialogue=True
        )

