# skills/base_skill.py


class BaseSkill:
    def __init__(self, agent=None, verbose=False):
        self.agent = agent
        self.verbose = verbose

    def execute(self, *args, **kwargs):
        """
        Méthode à implémenter par toutes les sous-classes.
        Elle doit contenir la logique principale du skill.
        """
        raise NotImplementedError("La méthode execute() doit être implémentée dans la sous-classe.")

