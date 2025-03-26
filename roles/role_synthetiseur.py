from roles.base_role import BaseRole

class RoleSynthetiseur(BaseRole):
    def __init__(self):
        objectif = "Fournir une synthèse objective et structurée d’un débat entre deux agents."
        super().__init__(name="Synthétiseur", objectif=objectif)

    def get_prompt(self) -> str:
        return (
            "Tu es un agent chargé de produire une synthèse neutre, claire et structurée d’un débat.\n"
            "Tu dois identifier les principaux arguments de chaque camp, les points de convergence ou divergence,\n"
            "et conclure par un résumé impartial. Tu ne prends pas parti."
        )
