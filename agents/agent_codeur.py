# agents/agent_codeur.py
from .base_agent import BaseAgent
from skills.coder.code_postprocessor_skill import CodePostProcessorSkill

class AgentCodeur(BaseAgent):
    def __init__(self, name, role, verbose=False, project_path="./temp_project"):
        super().__init__(name=name, role=role, verbose=verbose)
        self.project_path = project_path  # ✅ Gestion des fichiers projet

    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(CodePostprocessorSkill(agent=self, project_path=self.project_path, verbose=self.verbose))
        return skills