from .base_agent import BaseAgent
from roles.role_debateur import RoleDebateur
class AgentDebateur(BaseAgent):
    def __init__(self, name, role=RoleDebateur, verbose=False, camp=None):
        super().__init__(name=name, role=role, verbose=verbose)

    def init_default_skills(self):
        return super().init_default_skills()