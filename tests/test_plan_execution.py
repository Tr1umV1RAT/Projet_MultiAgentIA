# test/test_plan_execution.py

from skills.communication.messages import Message
from skills.reasoning import Reasoning
from skills.coder.code_postprocessor import CodePostProcessorSkill
from skills.planning.skill_planner import SkillPlanner
from skills.planning.plan_executor import PlanExecutorSkill
from tools.skill_manager import SkillManagerTool
from tools.memory_manager import MemoryManagerTool
from tools.archivage_tool import ArchivageTool
from skills.memory.long_term import LongTermMemory
import os

class DummyRole:
    def __init__(self, agent):
        self.outils = [ArchivageTool(agent=agent, verbose=True)]

class DummyAgent:
    def __init__(self):
        self.name = "TestAgent"
        self.project_path = "./temp_project"
        self.skills = []
        self.tools = []
        self.memoire_court_terme = None
        self.long_term_memory = LongTermMemory(db_path="long_term_test.db", verbose=True)
        self.role = None  # assigné après init pour passer self
        self.init()

    def init(self):
        self.skills = [
            Reasoning(agent=self, verbose=True),
            CodePostProcessorSkill(agent=self, verbose=True),
            SkillPlanner(agent=self, verbose=True),
            PlanExecutorSkill(agent=self, verbose=True)
        ]
        self.tools = [
            MemoryManagerTool(agent=self),
            SkillManagerTool(agent=self)
        ]
        self.role = DummyRole(agent=self)

    def get_skill(self, name):
        for s in self.skills:
            if type(s).__name__ == name:
                return s
        return None

if __name__ == "__main__":
    os.makedirs("./temp_project", exist_ok=True)
    agent = DummyAgent()

    message = Message(
        origine="ProjectManager",
        destinataire="TestAgent",
        type_message="task",
        contenu="# fichier: main.py\n```python\ndef hello():\n    print(\"Hello, world!\")\n```",
        memoriser=True
    )

    planner = agent.get_skill("SkillPlanner")
    plan_message = planner.handle_message(message)
    print("\n--- PLAN ---\n", plan_message)

    # On injecte manuellement l'archivage comme tool (pour forcer un plan hybride)
    plan_message.meta["plan"].append({
        "type": "tool",
        "name": "ArchivageTool",
        "objectif": "Archiver le message via un outil rattaché au rôle"
    })

    executor = agent.get_skill("PlanExecutorSkill")
    result = executor.handle_message(plan_message)
    print("\n--- RESULTAT ---\n", result)

    print("\n--- MEMOIRE LONG TERME ---")
    for m in agent.long_term_memory.recall(destinataire="TestAgent"):
        print(m)
