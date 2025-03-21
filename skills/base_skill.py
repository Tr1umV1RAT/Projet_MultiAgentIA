class BaseSkill:
    def __init__(self, name="Skill"):
        self.name = name

    def utiliser(self, *args, **kwargs):
        raise NotImplementedError("Cette méthode doit être implémentée dans une sous-classe")
