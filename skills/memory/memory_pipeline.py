import os
from skills.memory.short_term_memory import ShortTermMemory
from skills.memory.working_memory import WorkingMemory
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.memory_manager import MemoryManager
from skills.memory.memory_retriever import MemoryRetrieverSkill
from skills.communication.messages import Message

DEFAULT_MEMORY_CONFIG = {
    "use_short_term": True,
    "use_long_term": True,
    "store_output": True,
    "max_context_messages": 8
}

class MemoryPipeline:
    def __init__(self, agent_name: str, role=None, llm=None, config: dict = None, base_path: str = "agent_memories"):
        self.agent_name = agent_name
        self.role = role  # Peut être None
        self.llm = llm  # Requis pour working memory
        self.config = config or DEFAULT_MEMORY_CONFIG

        # Création du répertoire de mémoire si nécessaire
        self.memory_path = os.path.join(base_path, agent_name)
        os.makedirs(self.memory_path, exist_ok=True)

        # Initialisation des modules mémoire internes
        self.short_term = ShortTermMemory(agent_name)
        self.long_term = LongTermMemory(agent_name)
        self.working = WorkingMemory(llm=self.llm, long_term_memory=self.long_term)

        self.manager = MemoryManager(
            stm=self.short_term,
            ltm=self.long_term,
            wm=self.working,
            importance_threshold=1
        )

        self.retriever = MemoryRetrieverSkill(memory_access_strategy=None)  # temporairement sans stratégie

    def get_context(self, message: Message, team_context: str = None) -> str:
        """
        Construit le contexte complet à injecter dans un prompt :
        - Consignes de rôle (si disponible)
        - Contexte d'équipe (si fourni)
        - Historique de messages récents (short term)
        """
        blocks = []

        # Bloc de consigne du rôle
        if self.role and hasattr(self.role, "prompt"):
            blocks.append(f"[CONSIGNE DE RÔLE]\n{self.role.prompt}")

        # Bloc de contexte d'équipe si fourni
        if team_context:
            blocks.append(f"[CONTEXTE D'ÉQUIPE]\n{team_context.strip()}")

        # Bloc historique de discussion
        if self.config["use_short_term"]:
            recent = self.short_term.retrieve(query=None, max_results=self.config["max_context_messages"])

            if recent:
                discussion = "\n".join(
                    f"{m.origine}: {m.contenu}" for m in recent if getattr(m, "type_message", "text") == "text"

                )
                blocks.append(f"[HISTORIQUE]\n{discussion}")

        return "\n\n".join(blocks)

    def store_message(self, message: Message):
        if self.config["store_output"]:
            self.manager.store_message(message)


    def store_code(self, message: Message):
        if message.type == "code":
            self.manager.store_message(message)


    def search_long_term(self, query: str = "", top_k: int = 5):
        if self.config["use_long_term"]:
            return self.retriever.search_long_term(query, top_k=top_k)
        return []

    def clear_working_memory(self):
        self.working.clear()

    def set_role(self, role):
        self.role = role