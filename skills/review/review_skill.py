from skills.base_skill import BaseSkill
from tools.ollama_tool import OllamaTool  # Outil de raisonnement basé sur Ollama

class ReviewSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="ReviewSkill",
            description="Compétence pour analyser et améliorer le code fourni.",
            tools=[OllamaTool()]
        )

    def execute(self, code: str) -> str:
        """
        Analyse le code fourni et propose des améliorations.

        :param code: Le code source à analyser.
        :return: Suggestions d'amélioration.
        """
        prompt = f"""
        Tu es un expert en revue de code Python. Analyse le code suivant et propose des améliorations :

        ```python
        {code}
        ```

        Points à vérifier :
        - Respect des conventions PEP 8
        - Lisibilité et clarté
        - Présence de commentaires pertinents
        - Gestion des exceptions
        - Optimisation et efficacité

        Fournis des suggestions détaillées pour chaque point nécessitant une amélioration.
        """
        return self.tools[0].run(prompt)
