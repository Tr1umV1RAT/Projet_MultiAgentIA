import os
from datetime import datetime
from skills.base_skill import BaseSkill
from skills.memory.short_term_memory import ShortTermMemory
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.working_memory import WorkingMemory
from skills.memory.memory_manager import MemoryManager
from skills.memory.memory_retriever_skill import MemoryRetrieverSkill
from skills.memory.llm_memory_access import LLMMemoryAccess
from skills.communication.messages import Message

class MemorySkill(BaseSkill):
    def __init__(
        self, name, llm,
        base_path="agent_memories", verbose=False, importance_threshold=1
    ):
        super().__init__()
        self.name = "memory"
        self.agent_name = name
        self.verbose = verbose
        self.memory_path = self._create_unique_memory_directory(base_path)

        self.short_term = ShortTermMemory(name, self.memory_path)
        self.long_term = LongTermMemory(name, self.memory_path)
        self.working_memory = WorkingMemory(llm, self.long_term)

        memory_strategy = LLMMemoryAccess(llm, self.long_term, verbose=verbose)
        self.retriever = MemoryRetrieverSkill(memory_strategy, agent=name, verbose=verbose)

        self.manager = MemoryManager(
            self.short_term, self.long_term, self.working_memory, importance_threshold
        )

    def _create_unique_memory_directory(self, base_path):
        os.makedirs(base_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{self.agent_name}_{timestamp}"
        full_path = os.path.join(base_path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def update_short_term(self, messages):
        for message in messages:
            self.short_term.store(message)

    def compose_working_memory(self, query, max_results=3):
        return self.working_memory.retrieve(query, max_results)

    # Méthode améliorée pour afficher clairement les résultats
    def run(self, message: Message):
        query = message.contenu
        results = self.compose_working_memory(query, max_results=3)
        
        memory_summary = "\n".join(f"- {res.contenu}" for res in results if hasattr(res, 'contenu')) \
            if results else "(Aucune mémoire pertinente trouvée.)"

        response_message = Message(
            origine=self.agent_name,
            destinataire=message.origine,
            contenu=f"🧠 Mémoire pertinente pour '{query}':\n{memory_summary}",
            conversation_id=message.conversation_id,
            metadata={"skill_used": "memory"}
        )

        if self.verbose:
            print(f"[MemorySkill] run() exécuté avec le message : '{query}'")

        return response_message
