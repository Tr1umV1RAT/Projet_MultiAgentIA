# agents/agent_reviewer.py

# agents/agent_reviewer.py
from agents.base_agent import BaseAgent
from roles.team_reviewer_role import RoleTeamReviewer
from skills.review_skill import SkillReview
from skills.test_runner_skill import SkillTestRunner

class AgentReviewer(BaseAgent):
    def __init__(self, role=None, memory=None, verbose=False):
        role = role or RoleTeamReviewer()
        super().__init__(name="Reviewer", role=role, verbose=verbose)

        self.skill_review = SkillReview(self, verbose=verbose)
        self.skill_test = SkillTestRunner(self, verbose=verbose)

        self.skills.append(self.skill_review)
        self.skills.append(self.skill_test)

    def receive_message(self, message):
        # Si test demandé, exécute les tests AVANT la review
        if message.metadata.get("test") is True:
            test_result = self.skill_test.run(message)
            self.memory.store_message(test_result)

            if self.verbose:
                print(f"[Reviewer] Résultat des tests : {test_result.metadata.get('status')}")

        return self.review(message)

    def review(self, message):
        return self.skill_review.run(message)
