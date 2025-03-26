from agents.base_agent import BaseAgent
from roles.role_moderateur import RoleModerateur
from skills.reasoning import Reasoning
from skills.communication.communication import Communication
from skills.memory.memory_skill import MemorySkill

class AgentModerateur(BaseAgent):
    def __init__(self, name: str = "Modérateur", verbose: bool = False):
        role = RoleModerateur()
        super().__init__(name=name, role=role, verbose=verbose)

        self.skills.append(Reasoning)
        self.skills.append(self.communication)
        self.skills.append(self.memoire)

        # Logique future : tour de parole, timing, recentrage
        self.tour = 0  # compteur de round
