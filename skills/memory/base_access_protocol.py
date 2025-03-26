from abc import ABC, abstractmethod

class BaseAccessProtocol(ABC):
    @abstractmethod
    def is_authorized(self, reason: str = "") -> bool:
        pass

    @abstractmethod
    def log_access(self, action: str, meta: dict = None):
        pass

    @abstractmethod
    def read(self, long_term_memory, filtre: dict = None) -> list:
        pass
