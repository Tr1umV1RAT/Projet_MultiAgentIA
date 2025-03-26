from roles.base_role import BaseRole

class RoleDebateur(BaseRole):
    def __init__(self, camp: str):
        self.camp = camp.lower()
        objectif = f"Défendre le point de vue '{camp}' dans un débat en argumentant de manière rigoureuse."
        super().__init__(name=f"Débateur-{camp}", objectif=objectif)

    def get_prompt(self) -> str:
        return (
            f"Tu es un agent IA chargé de participer à un débat.\n"
            f"Tu représentes la position : '{self.camp.upper()}'.\n"
            f"Ton rôle est de défendre ce point de vue avec des arguments solides, sans jamais changer de position.\n"
            f"Réfute poliment mais fermement les arguments adverses. Ne dis jamais que tu es une IA.\n"
        )
