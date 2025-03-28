from skills.memory.base_memory import BaseMemory
from skills.communication.messages import Message

class ShortTermMemory(BaseMemory):
    def __init__(self, agent_name=None, memory_path=None):
        self.agent_name = agent_name
        self.memory_path = memory_path
        self.messages = []

    def store(self, message: Message):
        self.messages.append(message)

    def retrieve(self, query, max_results=10):
        return self.messages[-max_results:]

    def clear(self):
        self.messages.clear()
