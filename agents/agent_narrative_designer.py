from agents.base_agent import BaseAgent
from skills.narrative_skill import SkillNarrative

class AgentNarrativeDesigner(BaseAgent):
    def __init__(self, name="NarrativeDesigner", role=None, project_path="project_outputs", memory=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        self.skill_narrative = SkillNarrative(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            verbose=verbose
        )

    def narrate(self, objectif: str = None, code_en_cours: str = None, phase="initial") -> str:
        return self.skill_narrative.generate_narrative(
            objectif=objectif,
            code_en_cours=code_en_cours,
            phase=phase
        )

    def receive_message(self, message):
        if getattr(message, "action", None) == "narrate" or message.type_message == "code":
            feedback = self.narrate(
                objectif=message.metadata.get("objectif"),
                code_en_cours=message.contenu,
                phase=message.metadata.get("phase", "integration")
            )

            from skills.communication.messages import Message
            return Message(
                origine=self.name,
                destinataire="Codeur",
                contenu=feedback,
                action="coder",
                metadata={"context": "narrative feedback", "first_call": False},
                type_message="text"
            )

        return super().receive_message(message)
