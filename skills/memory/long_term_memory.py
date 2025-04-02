import os
import sqlite3
from skills.memory.base_memory import BaseMemory
from skills.communication.messages import Message

class LongTermMemory(BaseMemory):
    def __init__(self, agent_name=None, memory_path=None):
        self.agent_name = agent_name
        self.memory_path = memory_path
        self.db_path = os.path.join(memory_path, "long_term_memory.db") if memory_path else None
        self._init_db()

    def _init_db(self):
        if self.db_path:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    origine TEXT,
                    contenu TEXT
                )
            """)
            self.conn.commit()

    def store(self, message: Message):
        if self.db_path:
            self.cursor.execute("INSERT INTO memories (origine, contenu) VALUES (?, ?)", (message.origine, message.contenu))
            self.conn.commit()

    def retrieve(self, query, max_results=5):
        if self.db_path:
            self.cursor.execute("SELECT origine, contenu FROM memories ORDER BY id DESC LIMIT ?", (max_results,))
            rows = self.cursor.fetchall()
            messages = []
            for row in rows:
                msg = Message(origine=row[0], contenu=row[1])
                messages.append(msg)
            return messages
        return []

    def clear(self):
        if self.db_path:
            self.cursor.execute("DELETE FROM memories")
            self.conn.commit()
    @property
    def path(self):
        return self.db_path