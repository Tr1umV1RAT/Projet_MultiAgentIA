from agents.base_agent import BaseAgent
from roles.project_manager import ProjectManager
from skills.db_management.db_management import DBManagementSkill
from config import Config

class AgentManager(BaseAgent):
    def __init__(self, nom="AgentManager"):
        role = ProjectManager()
        memoire_persistante = DBManagementSkill(
            f"teams/{nom}/{nom}_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            overwrite=True,
            adapt_name_if_exists=True
        )

        super().__init__(nom=nom, role=role, memoire_persistante=memoire_persistante)

        # Skill de structuration (à venir)
        # self.skills.append(PlannerSkill())
