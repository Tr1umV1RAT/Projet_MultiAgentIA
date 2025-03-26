from .base_agent import BaseAgent
from skills.communication import Communication
from skills.reviewer.review_skill import ReviewSkill
class AgentReviewer(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(
            name=name,
            role=role,
            verbose=verbose,
            communication=Communication(verbose=verbose)
        )



    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(ReviewSkill(agent=self, verbose=self.verbose))
        return skills
