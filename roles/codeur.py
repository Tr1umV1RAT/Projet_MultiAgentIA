from roles.base_role import BaseRole
from tools.llm_adapter import LLMAdapterTool

class CodeurRole(BaseRole):
    def __init__(self):
        super().__init__(
            nom_role="CodeurBasique",
            objectif="Écrire du code fonctionnel d’après des instructions données par le Chef de Projet.",
            contexte="""
Tu es un codeur chargé de réaliser des tâches de programmation sur la base des instructions précises du chef de projet.
Tu dois produire un code clair, commenté si nécessaire, et respectant les spécifications fournies.
""",
            outils=[LLMAdapterTool()],
            instructions_specifiques="Toujours structurer le code avec des exemples pratiques."
        )
