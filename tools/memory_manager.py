# tools/memory_manager.py
# -*- coding: utf-8 -*-

from typing import List, Optional
from skills.communication.messages import Message
from skills.memory.short_term import ShortTermMemory
from skills.db_management.db_management import DBManagementSkill  # ou LongTermMemory
from tools.llm_adapter import LLMAdapterTool

class MemoryManagerTool:
    def __init__(self, agent):
        self.agent = agent
        self.short_term: Optional[ShortTermMemory] = getattr(agent, "memoire_court_terme", None)
        self.long_term: Optional[DBManagementSkill] = getattr(agent, "long_term_memory", None)

    def get_recent_messages(self, limit=5) -> List[Message]:
        if not self.short_term:
            return []
        return self.short_term.get_recent_history(limit=limit)

    def get_facts(self, type_info: Optional[str] = None, agent_name: Optional[str] = None):
        if not self.short_term:
            return []
        return self.short_term.recall(type_info=type_info, agent_name=agent_name)

    def save_to_long_term(self, message: Message):
        if not self.long_term:
            raise RuntimeError("Long term memory not available.")
        self.long_term.save_message(message)

    def query_long_term(self, type_message: Optional[str] = None, destinataire: Optional[str] = None, limit: int = 10):
        if not self.long_term:
            return []
        return self.long_term.get_by_type(destinataire=destinataire, type_message=type_message, limit=limit)

    def get_conversation(self, conversation_id: str):
        if not self.long_term:
            return []
        if hasattr(self.long_term, "get_by_conversation"):
            return self.long_term.get_by_conversation(conversation_id)
        return []

    def summarize_conversation(self, conversation_id: str, llm_tool: Optional[LLMAdapterTool] = None) -> str:
        messages = self.get_conversation(conversation_id)
        if not messages or not llm_tool:
            return ""
        contenu = "\n".join([f"{m.origine}: {m.contenu}" for m in messages])
        prompt = f"Resume la conversation suivante entre agents :\n{contenu}"
        return llm_tool.run(prompt)
