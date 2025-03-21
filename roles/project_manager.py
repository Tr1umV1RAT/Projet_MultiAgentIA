from roles.base_role import BaseRole
from tools.ollama_tool import OllamaTool

class ProjectManager(BaseRole):
    def __init__(self, objectif="Coordonner explicitement le projet de code.", outils=None):
        super().__init__(
            nom="Project_Manager",
            objectif="Coordonner l'équipe et gérer le déroulement explicite du projet de codage.",
            contexte="Tu es responsable de la planification et de la répartition des tâches entre développeurs, reviewers et autres acteurs du projet. Tu t'assures que les objectifs sont atteints dans les délais prévus.",
            outils=[Ollama()]  # outils à définir clairement selon tes besoins
        )
