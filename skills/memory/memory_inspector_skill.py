from skills.base_skill import BaseSkill
from .memory_inspector import MemoryInspector

class MemoryInspectorSkill(BaseSkill):
    def __init__(self, agent, verbose=False):
        super().__init__(agent=agent, verbose=verbose)
        db_path = f"agent_memories/{agent.name}_ltm.db"
        self.inspector = MemoryInspector(db_path=db_path)

    def inspect_recent(self, limit=10):
        memories = self.inspector.list_memories(limit=limit)
        self.inspector.pretty_display(memories)

    def inspect_query(self, query):
        memories = self.inspector.search_memories(query=query)
        self.inspector.pretty_display(memories)
