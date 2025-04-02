# agents/agent_codeur.py
from agents.base_agent import BaseAgent
from skills.coder_skill import SkillCoder

class AgentCodeur(BaseAgent):
    def __init__(self, name="Codeur", role=None, project_path="project_outputs", memory=None, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        self.skill_coder = SkillCoder(
            agent=self,
            project_path=project_path,
            memory=memory if memory else self.memory,
            verbose=verbose
        )

    def coder(self, instruction: str, context: str = None, first_call: bool = True):
        return self.skill_coder.generate_code(
            instruction=instruction,
            context=context,
            first_call=first_call
        )

    def receive_message(self, message):
        if getattr(message, "action", None) == "coder":
            context = message.metadata.get("context", "")
            previous_code = self.retriever.get_latest_validated_code()

            if previous_code:
                context += f"\n\n💾 CODE VALIDÉ PRÉCÉDEMMENT :\n{previous_code}"

            return self.coder(
                instruction=message.contenu,
                context=context,
                first_call=message.metadata.get("first_call", True)
            )

        return super().receive_message(message)
