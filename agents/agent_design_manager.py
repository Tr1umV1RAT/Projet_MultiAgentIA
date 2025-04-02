# agents/agent_design_manager.py

from agents.base_agent import BaseAgent
from skills.planning_skill import SkillPlanning

class AgentDesignManager(BaseAgent):
    def __init__(self, name="DesignManager", role=None, project_path="project_outputs", memory=None, memory_codeur=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        # Ajout manuel de la skill de planification
        self.skill_plan = SkillPlanning(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            memory_codeur=memory_codeur,
            verbose=verbose
        )
        self.skills.append(self.skill_plan)

    def plan(self, instruction: str):
        return self.skill_plan.generate_plan(objectif=instruction)

    def receive_message(self, message):
        if getattr(message, "action", None) == "plan":
            return self.plan(message.contenu)
        return super().receive_message(message)
