# agents/agent_reviewer.py

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
        self.skills.append(self.skill_review)

    def review(self, message):
        return self.skill_review.run(message)

    def receive_message(self, message):
        if message.metadata.get("action") == "review":
            return self.review(message)
        return super().receive_message(message)
