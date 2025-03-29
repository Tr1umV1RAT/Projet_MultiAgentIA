from agents.base_agent import BaseAgent
from skills.planning_skill import SkillPlanning

class AgentDesignManager(BaseAgent):
    def __init__(self, name="DesignManager", role=None, project_path="project_outputs", memory=None, memory_codeur=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        self.skill_planning = SkillPlanning(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            memory_codeur=memory_codeur,
            verbose=verbose
        )

    def plan(self, objectif: str) -> str:
        instruction = self.skill_planning.generate_plan(objectif)

        from skills.communication.messages import Message
        return Message(
            origine=self.name,
            destinataire="Codeur",
            contenu=instruction,
            action="coder",
            metadata={"context": "design instruction", "first_call": True},
            type_message="text"
        )

    def receive_message(self, message):
        if getattr(message, "action", None) == "plan":
            return self.plan(message.contenu)

        return super().receive_message(message)
