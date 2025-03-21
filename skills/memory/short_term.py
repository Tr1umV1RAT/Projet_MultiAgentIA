from skills.base_skill import BaseSkill

class ShortTermMemory(BaseSkill):
    def __init__(self):
        super().__init__("ShortTermMemory")
        self.memoires = []

    def save(self, contenu, agent_name=None, type_info=None):
        self.memoires.append({
            "agent_name": agent_name,
            "type_info": type_info,
            "contenu": contenu
        })

    def recall(self, agent_name=None, type_info=None, limit=10):
        resultats = [
            m for m in self.memoires
            if (agent_name is None or m["agent_name"] == agent_name) and
               (type_info is None or m["type_info"] == type_info)
        ]
        return resultats[-limit:]
