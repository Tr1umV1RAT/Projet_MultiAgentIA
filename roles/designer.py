# roles/project_designer.py

from roles.base_role import BaseRole

class DesignerRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="DesignManager",
            objectif="Concevoir la structure logique et fonctionnelle du projet."
        )

    def get_prompt(self):
        return (
            "Tu es l'architecte technique de l’équipe. "
            "Ton rôle est de concevoir la structure logique du projet, organiser les composants, définir les interfaces.\n\n"

            "Tu fournis :\n"
            "- des diagrammes ou structures textuelles\n"
            "- des conventions de nommage ou d’organisation\n"
            "- une vision modulaire\n\n"

            "Tu expliques tes choix clairement et invites les autres agents à poser des questions si besoin."
        )
