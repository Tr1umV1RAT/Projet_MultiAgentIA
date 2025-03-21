from skills.memory.short_term import ShortTermMemory
from skills.reasoning import Reasoning
from skills.communication.communication import Communication
import config

class BaseAgent:
    def __init__(self, name, role=None):
        """
        Initialise un agent avec un nom et un rôle optionnel.
        L'agent dispose d'une mémoire courte, d'une compétence de reasoning et d'un skill de communication.
        """
        self.name = name
        self.role = role
        self.memoire = ShortTermMemory()
        self.messages = []  # File de réception des messages.
        # Instancier le skill Communication en utilisant la config globale.
        self.communication = Communication(verbose=config.VERBOSE_COMMUNICATION)
        self.reasoning = Reasoning(self)

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
