from agents.base_agent import BaseAgent
from skills.project_synthesis_skill import SkillProjectSynthesis

class AgentProjectManager(BaseAgent):
    def __init__(self, name="ProjectManager", role=None, project_path="project_outputs", memory=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        self.skill_synthesis = SkillProjectSynthesis(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            verbose=verbose
        )

    def synthesize(self):
        return self.skill_synthesis.generate_synthesis()

    def dispatch_to_design(self, objectif: str):
        from skills.communication.messages import Message
        return Message(
            origine=self.name,
            destinataire="DesignManager",
            contenu=objectif,
            action="plan",
            metadata={"context": "initial project instruction"},
            type_message="text"
        )

    def receive_message(self, message):
        if getattr(message, "action", None) == "synthesis":
            return self.synthesize()

        return super().receive_message(message)
