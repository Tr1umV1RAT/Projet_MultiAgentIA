from skills.base_skill import BaseSkill

class ShortTermMemory:
    def __init__(self, agent_id: str, memory_path: str, max_length: int = 10):
        self.agent_id = agent_id
        self.memory_path = memory_path
        self.buffer = []
        self.max_length = max_length

    def add_messages(self, messages: list):
        """
        Ajoute une liste de messages à la mémoire court terme.
        """
        self.buffer.extend(messages)
        self.buffer = self.buffer[-self.max_length:]

    def get_context_summary(self) -> str:
        """
        Résume les derniers messages en un bloc de contexte (texte brut).
        """
        return "\n".join(str(msg) for msg in self.buffer)

    def store(self, message):
        """
        Stocke un message unique (utile en streaming).
        """
        self.add_messages([message])
