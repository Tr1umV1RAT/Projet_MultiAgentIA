from skills.communication import Communication
from skills.memory.short_term_memory import ShortTermMemory
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.working_memory import WorkingMemory
from skills.memory.memory_manager import MemoryManager
from skills.memory.memory_retriever import MemoryRetrieverSkill
from tools.llm_wrapper import LLMWrapper
from skills.communication.messages import Message

class BaseAgent:
    def __init__(self, name, role, skills=None, verbose=False, communication=None, llm=None, memory_enabled=True):
        self.name = name
        self.role = role
        self.verbose = verbose

        # Interface LLM (injectée ou créée automatiquement)
        self.llm = llm if llm else LLMWrapper(agent=self, verbose=verbose)

        # Mémoire intégrée par défaut, sauf indication contraire explicite
        if memory_enabled:
            self.init_memory()
        else:
            self.memory = None

        # Communication (injectée ou créée automatiquement)
        self.communication = communication if communication else Communication(verbose=verbose)

        # File d'attente de messages entrants
        self.messages = []

        # Skills supplémentaires
        self.retriever = MemoryRetrieverSkill(agent=self, verbose=verbose)
        self.skills = skills if skills else []
        self.skills += self.init_default_skills()

        if self.verbose:
            print(f"[Init] Agent {self.name} initialisé avec le rôle {self.role.name}")

    def init_default_skills(self):
        """Skills indispensables à tout agent par défaut."""
        default_skills = [self.communication, self.retriever]
        if self.memory:
            default_skills.append(self.memory)
        return default_skills

    def init_memory(self, base_path="agent_memories"):
        """Initialise automatiquement les mémoires (STM, LTM, WorkingMemory)."""
        stm = ShortTermMemory()
        ltm = LongTermMemory(db_path=f"{base_path}/{self.name}_ltm.db")
        wm = WorkingMemory(self.llm, ltm)
        self.memory = MemoryManager(stm, ltm, wm)

        if self.verbose:
            print(f"[Memory] Mémoire activée pour {self.name}.")

    def receive_message(self, message: Message):
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

            # Enregistrer le message entrant en mémoire si nécessaire
            if self.memory and getattr(message, "memoriser", True):
                self.memory.store_message(message)

            # Générer le contexte mémoire dynamique (Working Memory)
            contexte = self.retriever.build_context(message) if self.memory else ""

            # Préparer le prompt final pour LLM
            prompt_final = f"{self.role.get_prompt()}\nContexte: {contexte}\n{message.contenu}"

            # Générer la réponse via LLM
            response_contenu = self.llm.query(prompt_final)

            if self.verbose:
                print(f"[{self.name}] Réponse générée : {response_contenu}")

            # Créer le message de réponse
            response_msg = Message(
                origine=self.name,
                destinataire=message.origine,
                type_message="llm_response",
                contenu=response_contenu,
                dialogue=True,
                memoriser=True,
                metadata={"reponse_a": getattr(message, 'id', None)}
            )

            # Stocker la réponse dans la mémoire
            if self.memory:
                self.memory.store_message(response_msg)

            # Envoyer la réponse via Communication
            self.communication.send(response_msg)

    def get_prompt_context(self):
        """Retourne le prompt de rôle pour initialiser ou enrichir le contexte."""
        return self.role.get_prompt()

    @property
    def objectif(self):
        return getattr(self.role, "objectif", None)

    def __repr__(self):
        return f"<Agent {self.name} - Rôle: {self.role.name}>"

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:])

    if not prompt:
        print("Veuillez fournir un prompt.")
        sys.exit(1)

    from roles.base_role import BaseRole
    role = BaseRole(name="DefaultAgent", objectif="Conversation générale")
    agent = BaseAgent(name="AgentCLI", role=role)

    message_recu = Message(contenu=prompt, origine="user", destinataire="AgentCLI")
    agent.receive_message(message_recu)
    agent.process_messages()