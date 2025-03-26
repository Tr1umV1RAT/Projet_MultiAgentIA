from typing import List
from skills.communication.messages import Message
from .base_memory import BaseMemory
from tools.llm_interface import LLMInterface

class WorkingMemory(BaseMemory):
    def __init__(self, llm_adapter: LLMInterface, long_term_memory: LongTermMemory):
        self.llm = llm_adapter
        self.ltm = long_term_memory

    def store(self, message: Message):
        pass  # La WorkingMemory ne stocke pas directement

    def retrieve(self, query: str, max_results: int = 5) -> List[Message]:
        # Utiliser LLM pour générer une synthèse contextuelle
        retrieved = self.ltm.retrieve(query, max_results=20)
        synthesis = self.llm.synthesize_context([msg.contenu for msg in retrieved])
        return [Message(contenu=synthesis)]

    def clear(self):
        pass  # La WorkingMemory est dynamique et ne nécessite pas de nettoyage
