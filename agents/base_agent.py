from skills.communication import Communication
from skills.memory.memory_skill import MemorySkill
from tools.llm_wrapper import LLMWrapper
from skills.communication.messages import Message

class BaseAgent:
    def __init__(self, name, role, skills=None, verbose=False, communication=None, llm=None):
        self.name = name
        self.role = role  # Instance de BaseRole ou dérivée
        self.verbose = verbose

        # Interface LLM (injectée ou créée)
        self.llm = llm if llm is not None else LLMWrapper(agent=self, verbose=verbose)

        # Mémoire complète (short + long + mémoire immédiate)
        self.init_memory()

        # Communication (skill) injectée ou par défaut
        self.communication = communication if communication is not None else Communication(verbose=verbose)

        # File d'attente de messages entrants
        self.messages = []

        # Ensemble des skills
        self.skills = skills if skills is not None else []
        self.skills += self.init_default_skills()

        if self.verbose:
            print(f"[Init] Agent {self.name} initialisé avec le rôle {self.role.name}")

    def init_default_skills(self):
        """Ajoute les skills indispensables à tout agent."""
        return [self.communication, self.memoire]

    def receive_message(self, message):
        """Ajoute un message à la file d'attente."""
        self.messages.append(message)
        if self.verbose:
            print(f"[{self.name}] Message reçu : {message}")

    def process_messages(self):
        """Traite tous les messages en attente via les skills disponibles."""
        while self.messages:
            message = self.messages.pop(0)

            if message.origine == self.name and message.type_message == "llm_response":
                if self.verbose:
                    print(f"[{self.name}] ⏩ Auto-réponse ignorée.")
                continue

            if self.verbose:
                print(f"[{self.name}] Traitement du message : {message}")

            # 1. 🧠 Enregistrer le message entrant s’il doit être mémorisé
            if getattr(message, "memoriser", True):
                self.memoire.save_interaction(message)

            # 2. 🧠 Actualiser la mémoire court terme
            self.memoire.update_short_term([message])

            # 3. 🧠 Contexte mémoire pour génération
            working_context = self.memoire.compose_working_memory()
            prompt = f"{self.get_prompt_context()}\n\n{working_context}\n\nMessage reçu : {message.contenu}"

            # 4. 🧠 Génération via LLM
            if hasattr(self.llm, "ask"):
                raw_response = self.llm.ask(prompt)
                contenu = getattr(raw_response, "contenu", str(raw_response))
            elif hasattr(self.llm, "query"):
                contenu = self.llm.query(prompt)
            else:
                contenu = "[ERREUR: aucun LLM compatible]"

            if self.verbose:
                print(f"[{self.name}] Réponse générée : {contenu}")

            # 5. 💬 Créer un message de réponse
            response_msg = Message(
                origine=self.name,
                destinataire=message.origine,
                type_message="llm_response",
                contenu=contenu,
                dialogue=True,
                memoriser=True,
                meta={"reponse_a": message.id}
            )

            # 6. 🧠 Enregistrement mémoire de la réponse
            self.memoire.save_interaction(response_msg)

            # 7. 📨 Envoi via communication
            self.communication.send(response_msg)

    def get_prompt_context(self):
        """Récupère le prompt de rôle (peut être enrichi avec de la mémoire externe si besoin)."""
        return self.role.get_prompt()

    @property
    def objectif(self):
        return getattr(self.role, "objectif", None)

    def __repr__(self):
        return f"<Agent {self.name} - Rôle: {self.role.name}>"

    def init_memory(self, base_path: str = "agent_memories", reuse: bool = False):
        """
        Réinitialise la mémoire de l'agent avec des options spécifiques.
        Si reuse=True, recharge la dernière mémoire existante.
        """
        from skills.memory.memory_skill import MemorySkill
        if reuse:
            from skills.memory.long_term import LongTermMemory
            path = LongTermMemory(self.name, base_path=base_path, reuse=True).memory_path
            self.memoire = MemorySkill(
                agent_name=self.name,
                llm=self.llm,
                base_path=path,
                verbose=self.verbose
            )
        else:
            self.memoire = MemorySkill(
                agent_name=self.name,
                llm=self.llm,
                base_path=base_path,
                verbose=self.verbose
            )
