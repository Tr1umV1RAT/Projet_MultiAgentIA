from abc import ABC, abstractmethod

class BaseTool(ABC):
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, prompt: str) -> str:
        """
        Méthode à implémenter par chaque outil spécifique.
        :param prompt: Le texte d'entrée pour l'outil.
        :return: La réponse générée par l'outil.
        """
        pass
