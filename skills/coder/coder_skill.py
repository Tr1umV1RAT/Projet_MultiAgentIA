from skills.base_skill import BaseSkill

class CoderSkill(BaseSkill):
    def __init__(self, tools):
        super().__init__(
            name="CoderSkill",
            description="Compétence pour générer du code en fonction des spécifications fournies.",
            tools=tools
        )

    def execute(self, specifications: str) -> str:
        """
        Génère du code basé sur les spécifications fournies.
        :param specifications: Les spécifications détaillées du code à écrire.
        :return: Le code source généré.
        """
        if not self.tools:
            raise ValueError("Aucun outil LLM n'est disponible pour exécuter cette compétence.")
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

