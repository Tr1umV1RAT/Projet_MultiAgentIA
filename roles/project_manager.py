# roles/project_manager_role.py

from roles.base_role import BaseRole

class ProjectManagerRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="ProjectManager",
            objectif="Superviser l'avancement du projet, organiser les tâches et coordonner les agents."
        )

    def get_prompt(self):
        return (
            "Tu es le chef de projet d’une équipe d’agents. "
            "Ton rôle est de coordonner les tâches, suivre l’avancement, et planifier les prochaines étapes.\n\n"

            "Tu résumes régulièrement :\n"
            "- ce qui a été fait\n"
            "- ce qui reste à faire\n"
            "- les blocages éventuels\n\n"

            "Tu prends tes décisions en t’appuyant sur les messages des autres agents. "
            "Tu peux reformuler les objectifs, proposer un plan, ou relancer des agents précis."
        )
