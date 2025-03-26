from agents.base_agent import BaseAgent
from skills.communication import Communication

class AgentNarrateur(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(
            name=name,
            role=role,
            verbose=verbose,
            communication=Communication(verbose=verbose)
        )

    def init_default_skills(self):
        skills = super().init_default_skills()
        # Ajouter ici les skills spécifiques au narrateur
        return skills
