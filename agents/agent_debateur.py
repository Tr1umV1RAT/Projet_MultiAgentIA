from agents.base_agent import BaseAgent
from roles.role_debateur import RoleDebateur
from skills.reasoning import Reasoning
from skills.communication.communication import Communication
from skills.memory.memory_skill import MemorySkill

class AgentDebateur(BaseAgent):
    def __init__(self, name: str, camp: str, verbose: bool = False):
        role = RoleDebateur(camp)
        super().__init__(name=name, role=role, verbose=verbose)

        self.skills.append(Reasoning)
        self.skills.append(self.communication)  # dédoublé pour cohérence
        self.skills.append(self.memoire)  # intégration mémoire complète
