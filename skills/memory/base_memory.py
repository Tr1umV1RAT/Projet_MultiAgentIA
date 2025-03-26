from abc import ABC, abstractmethod
from typing import List
from skills.communication.messages import Message

class BaseMemory(ABC):
    @abstractmethod
    def store(self, message: Message):
        """Stocker un message en mémoire."""
        pass

    @abstractmethod
    def retrieve(self, query: str, max_results: int) -> List[Message]:
        """Récupérer des messages pertinents en fonction d'une requête."""
        pass

    @abstractmethod
    def clear(self):
        """Vider la mémoire."""
        pass
