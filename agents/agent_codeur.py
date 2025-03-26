from agents.base_agent import BaseAgent
from skills.communication import Communication
from skills.coder.code_postprocessor import CodePostProcessorSkill
class AgentCodeur(BaseAgent):
    def __init__(self, name, role, verbose=False, project_path="./temp_project"):
        super().__init__(name=name, role=role, verbose=verbose)
        self.project_path = project_path  # ✅ nécessaire pour le skill de postprocessing

    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(CodePostProcessorSkill(agent=self, verbose=self.verbose))
        return skills