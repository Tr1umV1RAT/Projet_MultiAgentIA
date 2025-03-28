from .base_agent import BaseAgent
from roles.role_moderateur import RoleModerateur
class AgentModerateur(BaseAgent):
    def __init__(self, name, role=RoleModerateur, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

    def init_default_skills(self):
        return super().init_default_skills()
