from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Génère une réponse basée sur le prompt fourni.
        :param prompt: Le texte d'entrée pour le LLM.
        :return: La réponse générée par le LLM.
        """
        pass
