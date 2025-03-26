from .base_agent import BaseAgent
from skills.communication import Communication
from skills.planning.planification_skill import PlanificationSkill
class AgentProjectManager(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(
            name=name,
            role=role,
            verbose=verbose,
            communication=Communication(verbose=verbose)
        )

    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(PlanificationSkill(agent=self, verbose=self.verbose))
        return skills
