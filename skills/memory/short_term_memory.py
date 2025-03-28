import os
from skills.memory.base_memory import BaseMemory
from skills.communication.messages import Message

class ShortTermMemory(BaseMemory):
    def __init__(self, agent_name=None, memory_path=None):
        self.agent_name = agent_name
        self.memory_path = memory_path
        self.messages = []
        self._file_path = os.path.join(self.memory_path, "short_term_memory.txt") if self.memory_path else None
        self._load_from_file()

    def store(self, message: Message):
        self.messages.append(message)
        self._save_to_file()

    def retrieve(self, query, max_results=5):
        # Pour simplifier, on retourne les derniers messages stockés.
        return self.messages[-max_results:]

    def clear(self):
        self.messages.clear()
        self._save_to_file()

    def _save_to_file(self):
        if self._file_path:
            with open(self._file_path, "w", encoding="utf-8") as f:
                for msg in self.messages:
                    # On sauvegarde simplement l'origine et le contenu
                    f.write(f"{msg.origine}: {msg.contenu}\n")

    def _load_from_file(self):
        if self._file_path and os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                from skills.communication.messages import Message
                for line in lines:
                    if ": " in line:
                        origine, contenu = line.split(": ", 1)
                        msg = Message(origine=origine.strip(), contenu=contenu.strip())
                        self.messages.append(msg)
