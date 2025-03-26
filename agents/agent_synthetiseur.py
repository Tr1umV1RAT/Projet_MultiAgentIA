from agents.base_agent import BaseAgent
from skills.communication import Communication
from skills.synthetiseur.synthese_skill import SyntheseSkill
class AgentSynthetiseur(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(
            name=name,
            role=role,
            verbose=verbose,
            communication=Communication(verbose=verbose)
        )

    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(SyntheseSkill(agent=self, verbose=self.verbose))
        # Ajouter ici les skills spécifiques au synthétiseur (ex: SyntheseSkill)
        return skills
