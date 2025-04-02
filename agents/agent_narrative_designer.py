# agents/agent_narrative_designer.py

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
        self.skills.append(self.skill_narrative)

    def narrate(self, message):
        return self.skill_narrative.run(message)

    def receive_message(self, message):
        # Si le message contient du code, proposer un feedback narratif
        if message.metadata.get("type") == "code":
            feedback = self.narrate(message)
            # renvoie un message avec action="coder" pour boucler avec le codeur
            feedback.metadata["action"] = "coder"
            return feedback

        # Sinon, traiter comme une demande de création narrative initiale
        if message.metadata.get("action") == "narrate":
            return self.narrate(message)

        return super().receive_message(message)
