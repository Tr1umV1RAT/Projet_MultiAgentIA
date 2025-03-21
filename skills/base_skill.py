from abc import ABC, abstractmethod
from typing import List
from tools.base_tool import BaseTool

class BaseSkill(ABC):
    def __init__(self, name: str, description: str = "", tools: List[BaseTool] = None):
        self.name = name
        self.description = description
        self.tools = tools or []

    @abstractmethod
    def execute(self, prompt: str) -> str:
        """
        Méthode à implémenter par chaque compétence spécifique.
        :param prompt: Le texte d'entrée pour la compétence.
        :return: La réponse générée par la compétence.
        """
        pass
