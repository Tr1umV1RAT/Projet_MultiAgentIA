from .base_agent import BaseAgent
from roles.role_synthetiseur import RoleSynthetiseur
class AgentSynthetiseur(BaseAgent):
    def __init__(self, name, role=RoleSynthetiseur, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

    def init_default_skills(self):
        return super().init_default_skills()
