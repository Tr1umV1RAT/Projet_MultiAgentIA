class BaseTool:
    def __init__(self, name="Tool"):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError("La méthode run() doit être implémentée.")
