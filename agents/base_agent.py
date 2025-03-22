from skills.memory.short_term import ShortTermMemory
from skills.reasoning import Reasoning
from skills.communication.communication import Communication
import config

class BaseAgent:
    def __init__(self, name, role=None, memoire=None, skills=None):
        """
        Initialise un agent avec un nom, un rôle optionnel, et une mémoire optionnelle.
        Par défaut, on utilise ShortTermMemory. Mais une LongTermMemory peut être injectée.
        """
        self.name = name
        self.role = role
        self.memoire = memoire if memoire is not None else ShortTermMemory()
        self.messages = []
        self.communication = Communication(verbose=config.VERBOSE_COMMUNICATION)
        self.reasoning = Reasoning(self)
        self.skills = skills or []  # Liste de skills associés

    def get_skill(self, skill_class):
        """
        Récupère le skill correspondant à la classe demandée.
        """
        for skill in self.skills:
            if isinstance(skill, skill_class):
                return skill
        raise ValueError(f"Skill {skill_class.__name__} introuvable pour l'agent {self.name}")

    def process_messages(self):
        """
        Traite les messages présents dans la file de réception.
        Pour chaque message, ajoute son contenu à la mémoire conversationnelle, 
        génère une réponse via le module Reasoning et l'envoie via Communication.
        """
        while self.messages:
            msg = self.messages.pop(0)
            self.memoire.add_message(f"{msg.expediteur}: {msg.contenu}")
            response = self.reasoning.reflechir(msg)
            self.communication.envoyer(response)
