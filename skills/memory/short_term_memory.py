from collections import deque
from typing import List
from skills.communication.messages import Message
from .base_memory import BaseMemory

class ShortTermMemory(BaseMemory):
    def __init__(self, max_size=10):
        self.memory = deque(maxlen=max_size)

    def store(self, message: Message):
        self.memory.append(message)

    def retrieve(self, query: str = "", max_results: int = 5) -> List[Message]:
        # Simple récupération des derniers messages (améliorable)
        return list(self.memory)[-max_results:]

    def clear(self):
        self.memory.clear()
