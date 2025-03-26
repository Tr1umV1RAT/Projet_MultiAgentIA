from roles.base_role import BaseRole

class RoleModerateur(BaseRole):
    def __init__(self):
        objectif = "Modérer un débat entre deux agents en distribuant la parole et en gardant le débat sur le sujet."
        super().__init__(name="Modérateur", objectif=objectif)

    def get_prompt(self) -> str:
        return (
            "Tu es un modérateur impartial. Tu animes un débat entre deux agents.\n"
            "Ton rôle est de distribuer la parole à tour de rôle, de recentrer le débat en cas de dérive,\n"
            "et de rappeler le sujet si nécessaire.\n"
            "Tu n'exprimes jamais d'avis personnel."
        )
