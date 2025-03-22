from agents.base_agent import BaseAgent
from skills.memory.short_term import ShortTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from messages import Message
from roles.reviewer import ReviewerRole


class AgentReviewer(BaseAgent):
    def __init__(self, nom="AgentReviewer", role=None, memoire_persistante=None):
        role = role or ReviewerRole()
        super().__init__(
            name=nom,
            role=role,
            memoire_persistante=memoire_persistante,
            skills=[
                ShortTermMemory(),
                Communication(verbose=Config.VERBOSE_COMMUNICATION),
                DBManagementSkill(db_name=f"{nom.lower()}_memory.db", schema=Config.MEMORY_TABLE_SCHEMA)
            ]
        )

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide ou vide. Veuillez soumettre un contenu à relire.",
                meta={"error": "Invalid message"}
            )

        # On construit un prompt d'évaluation critique.
        prompt = f"""
Tu es un reviewer professionnel. Voici les critères d'évaluation :

1. Clarté du code ou contenu fourni
2. Respect des consignes du prompt
3. Qualité de la documentation (docstrings, nommage clair, etc.)
4. Cohérence fonctionnelle
5. Améliorations possibles

Travail à analyser :
{message.contenu}
"""
        message_for_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "review_request", "original_task": message.meta.get("task", "")}
        )

        result = self.reasoning.reflechir(message_for_llm)

        # Enregistrement de l'avis dans la base
        db = self.get_skill(DBManagementSkill)
        db.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": "review", "review_of": message.meta.get("filename", "unknown")}
        ))

        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Voici mon avis sur le fichier {message.meta.get('filename', 'inconnu')} :\n\n{result.contenu}",
            dialogue=True
        )
