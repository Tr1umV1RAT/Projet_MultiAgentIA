# agents/base_agent.py
from skills.memory.short_term import ShortTermMemory
from skills.communication.communication import Communication
from skills import reasoning
from skills.reasoning import Reasoning
import config

class BaseAgent:
    def __init__(self, name, role=None, skills=None, verbose=False):
        """
        Initialise un agent avec un nom, un rôle optionnel, une liste de compétences et un mode verbeux.
        :param name: Nom de l'agent
        :param role: Rôle de l'agent (optionnel)
        :param skills: Liste de compétences associées à l'agent (optionnel)
        :param verbose: Booléen pour activer le mode verbeux
        """
        self.name = name
        self.role = role
        self.skills = skills or []
        self.verbose = verbose
        self.messages = []  # File de réception des messages.

        # Instanciation par défaut d'une communication
        self.communication = Communication(verbose=config.VERBOSE_COMMUNICATION)
        # Le module de reasoning pourra être initialisé dans l'agent s'il en a besoin.
        self.reasoning = None


    def process_messages(self):
        """
        Traite les messages dans la file de réception.
        Chaque message est traité une seule fois par cet agent, grâce à un marquage dans `meta['processed_by']`.
        """
        while self.messages:
            msg = self.messages.pop(0)
            # Assurer que le champ 'processed_by' existe
            if 'processed_by' not in msg.meta:
                msg.meta['processed_by'] = []
            # Si cet agent a déjà traité ce message, on passe
            if self.name in msg.meta['processed_by']:
                continue
            # Marquer ce message comme traité par cet agent
            msg.meta['processed_by'].append(self.name)
            # Sauvegarder le contenu dans la mémoire courte
            self.memoire_court_terme.add_message(f"{msg.expediteur}: {msg.contenu}")
            # Générer la réponse via reasoning (qui doit avoir été initialisé)
            response = self.reasoning.reflechir(msg)
            self.communication.envoyer(response)


    def get_skill(self, skill_class):
        """
        Récupère le skill correspondant à la classe demandée.
        """
        for skill in self.skills:
            if isinstance(skill, skill_class):
                return skill
        raise ValueError(f"Skill {skill_class.__name__} introuvable pour l'agent {self.name}")

