from skills.base_skill import BaseSkill
from tools.ollama_tool import OllamaTool  # Outil de génération de code basé sur Ollama

class CoderSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="CoderSkill",
            description="Compétence pour générer du code en fonction des spécifications fournies.",
            tools=[OllamaTool()]
        )

    def execute(self, specifications: str) -> str:
        """
        Génère du code basé sur les spécifications fournies.

        :param specifications: Les spécifications détaillées du code à écrire.
        :return: Code source généré.
        """
        prompt = f"""
        Tu es un développeur Python expérimenté. Écris du code en suivant ces spécifications :

        {specifications}

        Assure-toi que le code :
        - Respecte les conventions PEP 8
        - Est bien commenté
        - Gère les exceptions appropriées
        - Est optimisé pour l'efficacité
        """
        return self.tools[0].run(prompt)
