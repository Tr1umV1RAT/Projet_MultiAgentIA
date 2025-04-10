import os
from skills.communication.messages import Message

class ShortTermMemory:
    def __init__(self, agent_name=None, memory_path=None):
        self.agent_name = agent_name or "default_agent"
        self.memory_path = memory_path or os.path.join("agent_memories", self.agent_name, "short_term_memory.txt")
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)

    def store(self, message: Message):
        with open(self.memory_path, "a", encoding="utf-8") as f:
            f.write(f"{message.origine} ||| {message.contenu}\n")

    def retrieve(self, query=None, max_results=5):
        messages = []
        if not os.path.exists(self.memory_path):
            return messages

        with open(self.memory_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-max_results:]

        for line in lines:
            parts = line.strip().split(" ||| ")
            if len(parts) == 2:
                origine, contenu = parts
                msg = Message.text(
                    expediteur=origine.strip(),
                    destinataire=self.agent_name,
                    contenu=contenu.strip()
                )

                messages.append(msg)

        return messages