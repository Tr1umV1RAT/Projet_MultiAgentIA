from .base_agent import BaseAgent

class AgentDesigner(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

    def init_default_skills(self):
        return super().init_default_skills()
