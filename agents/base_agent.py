# agents/base_agent.py
from skills.communication import Communication
from skills.memory.short_term import ShortTermMemory

class BaseAgent:
    def __init__(self, name, role, skills=None, verbose=False, communication=None):
        self.name = name
        self.role = role
        self.verbose = verbose
        self.skills = skills if skills is not None else []
        # Injection de l'objet Communication
        self.communication = communication if communication is not None else Communication(verbose=verbose)
        # Instanciation de la mémoire court-terme par défaut
        self.memoire_court_terme = ShortTermMemory()
        # On peut ajouter ici les compétences par défaut si besoin
        self.skills += self.init_default_skills()

    @property
    def memoire(self):
        """Propriété unifiée pour accéder à la mémoire de l'agent."""
        return self.memoire_court_terme

    def init_default_skills(self):
        """Retourne une liste de compétences communes (pour l'instant, juste la communication)."""
        return [self.communication]

    def process_messages(self):
        """
        Méthode de traitement des messages.
        Elle devrait être implémentée pour récupérer et traiter les messages via les skills.
        """
        # Exemple : traiter chaque message de la file de messages
        while hasattr(self, 'messages') and self.messages:
            message = self.messages.pop(0)
            # Utilise Reasoning ou un autre skill pour traiter le message
            # Ici, on peut simplement appeler une méthode de traitement du message
            pass