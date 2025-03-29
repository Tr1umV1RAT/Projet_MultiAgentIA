from agents.base_agent import BaseAgent
from skills.review_skill import SkillReview

class AgentReviewer(BaseAgent):
    def __init__(self, name="Reviewer", role=None, project_path="project_outputs", memory=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        self.skill_review = SkillReview(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            verbose=verbose
        )

    def review(self, code: str) -> str:
        feedback = self.skill_review.review_code(code)

        from skills.communication.messages import Message
        return Message(
            origine=self.name,
            destinataire="Codeur",
            contenu=feedback,
            action="coder",
            metadata={"context": "review feedback", "first_call": False},
            type_message="text"
        )

    def receive_message(self, message):
        if getattr(message, "action", None) == "review":
            return self.review(message.contenu)

        return super().receive_message(message)
