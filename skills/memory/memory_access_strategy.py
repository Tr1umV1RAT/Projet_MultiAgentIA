from abc import ABC, abstractmethod

class MemoryAccessStrategy(ABC):
    @abstractmethod
    def retrieve(self, current_message, short_term_context=""):
        pass
