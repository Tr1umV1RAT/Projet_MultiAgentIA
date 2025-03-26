# agents/base_agent.py

from skills.communication import Communication
from skills.memory.short_term import ShortTermMemory
from tools.llm_wrapper import LLMWrapper

class BaseAgent:
    def __init__(self, name, role, skills=None, verbose=False, communication=None):
        self.name = name
        self.role = role  # Instance de BaseRole ou dérivée
        self.verbose = verbose

        # Communication est un skill à part entière, mais on l'injecte directement aussi
        self.communication = communication if communication is not None else Communication(verbose=verbose)

        # Mémoire court terme
        self.memoire_court_terme = ShortTermMemory()

        # Skills (reasoning, db_management, etc.)
        self.skills = skills if skills is not None else []
        self.skills += self.init_default_skills()

        # File d'attente de messages entrants
        self.messages = []

        # Interface LLM (présente par défaut)
        self.llm = LLMWrapper(agent=self, verbose=verbose)

        if self.verbose:
            print(f"[Init] Agent {self.name} initialisé avec le rôle {self.role.name}")

    @property
    def memoire(self):
        """Accès unifié à la mémoire (court terme pour l’instant)."""
        return self.memoire_court_terme

    def init_default_skills(self):
        """Ajoute les skills indispensables à tout agent."""
        return [self.communication]

    def receive_message(self, message):
        """Ajoute un message à la file d'attente."""
        self.messages.append(message)
        if self.verbose:
            print(f"[{self.name}] Message reçu : {message}")

    def process_messages(self):
        """Traite tous les messages en attente via les skills disponibles."""
        while self.messages:
            message = self.messages.pop(0)
            if self.verbose:
                print(f"[{self.name}] Traitement du message : {message}")

            handled = False
            for skill in self.skills:
                if hasattr(skill, "handle_message"):
                    result = skill.handle_message(message, agent=self)
                    if result is not None:
                        self.memoire.store(message, result)
                        handled = True
                        if self.verbose:
                            print(f"[{self.name}] Résultat traité par {type(skill).__name__}")
                        break  # Un seul skill répond, sauf si comportement multi-skill voulu

            if not handled and self.verbose:
                print(f"[{self.name}] Aucun skill n’a pu traiter le message.")

    def get_prompt_context(self):
        """Récupère le prompt de rôle (peut être enrichi)."""
        return self.role.get_prompt()

    @property
    def objectif(self):
        return getattr(self.role, "objectif", None)

    def __repr__(self):
        return f"<Agent {self.name} - Rôle: {self.role.name}>"
