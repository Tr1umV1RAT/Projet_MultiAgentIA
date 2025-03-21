class Message:
    def __init__(
        self, origine, destinataire, contenu, importance=1,
        memoriser=True, dialogue=False, affichage_force=False,
        action=None, type_message=None
    ):
        self.origine = origine
        self.destinataire = destinataire
        self.contenu = contenu
        self.importance = importance
        self.memoriser = memoriser
        self.dialogue = dialogue
        self.affichage_force = affichage_force
        self.action = action
        self.type_message = type_message
