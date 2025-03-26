# agents/agent_narrative_designer.py

from agents.base_agent import BaseAgent
from roles.narrative_designer import NarrativeDesignerRole
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from config import Config
from skills.communication.messages import Message
from skills.reasoning import Reasoning

class AgentNarrativeDesigner(BaseAgent):
    def __init__(self, nom="AgentNarrativeDesigner", role=None, memoire_persistante=None, verbose=False):
        role = role or NarrativeDesignerRole()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication(verbose=verbose)
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="narrative_designer_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante pour le design narratif"
        )
        self.db_skill = DBManagementSkill(db_name="narrative_designer_memory.db", schema=Config.MEMORY_TABLE_SCHEMA)
        skills = [self.memoire_court_terme, self.communication, self.db_skill, self.memoire_persistante]
        super().__init__(name=nom, role=role, skills=skills, verbose=verbose)
        self.reasoning = Reasoning(self)
        if self.verbose:
            print(f"[{self.name} INIT] Agent NarrativeDesigner initialisé en mode verbeux.")

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide reçu. Fournis-moi un thème ou un univers pour construire le scénario.",
                meta={"error": "invalid_input"},
                dialogue=True
            )
        prompt = f"""
Tu es un expert en design narratif. Tu dois créer une structure scénaristique cohérente, immersive et motivante.
Respecte ces éléments :
- Propose un univers original et cohérent
- Décris les personnages principaux
- Présente un arc narratif avec des rebondissements
- Anticipe les mécaniques interactives si c’est un jeu
- Termine par des pistes d'évolution future du scénario

Contexte / Commande :
{message.contenu}
"""
        msg_llm = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "narrative_generation"}
        )
        result = self.reasoning.reflechir(msg_llm)
        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=result.contenu,
            meta={"type_message": "narration"},
            dialogue=False
        ))
        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Scénario proposé :\n\n{result.contenu}",
            meta={"instruction": "narrative_generation"},
            dialogue=True
        )

