from collections import deque
from typing import List
from .base_memory import BaseMemory
from skills.communication.messages import Message

class ShortTermMemory(BaseMemory):
    def __init__(self, max_size=10):
        self.memory = deque(maxlen=max_size)

    def store(self, message: Message):
        self.memory.append(message)

    def retrieve(self, query: str = "", max_results: int = 5) -> List[Message]:
        return list(self.memory)[-max_results:]

    def clear(self):
        self.memory.clear()
