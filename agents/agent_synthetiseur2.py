from agents.base_agent import BaseAgent
from roles.role_synthetiseur import RoleSynthetiseur
from skills.reasoning.reasoning import ReasoningSkill
from skills.communication.communication import Communication
from skills.memory.memory_skill import MemorySkill

class AgentSynthetiseur(BaseAgent):
    def __init__(self, name: str = "Synthétiseur", verbose: bool = False):
        role = RoleSynthetiseur()
        super().__init__(name=name, role=role, verbose=verbose)

        self.skills.append(ReasoningSkill())
        self.skills.append(self.communication)
        self.skills.append(self.memoire)

    def produire_synthese(self):
        messages = self.memoire.short_term.buffer
        contenu = "\n".join(str(msg) for msg in messages)
        prompt = f"Fais une synthèse du débat suivant :\n{contenu}"
        return self.llm.ask(prompt)
