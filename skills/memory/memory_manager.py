# memory_manager.py

from skills.communication.messages import Message
from skills.memory.short_term_memory import ShortTermMemory
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.working_memory import WorkingMemory


class MemoryManager:
    def __init__(
        self, 
        stm: ShortTermMemory, 
        ltm: LongTermMemory, 
        wm: WorkingMemory
    ):
        self.stm = stm
        self.ltm = ltm
        self.wm = wm

    def store_message(self, message: Message):
        self.stm.store(message)
        if message.importance >= 5:
            self.ltm.store(message)

    def get_context(self, query: str) -> Message:
        return self.wm.retrieve(query)[0]

    def clear_all(self):
        self.stm.clear()
        self.ltm.clear()
