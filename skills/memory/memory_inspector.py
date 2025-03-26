import sqlite3
import json

class MemoryInspector:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def list_memories(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def search_memories(self, query):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories WHERE content LIKE ?", (f'%{query}%',))
        return cursor.fetchall()

    def pretty_display(self, memories):
        for memory in memories:
            print(json.dumps({
                "id": memory[0],
                "content": memory[1],
                "importance": memory[2],
                "timestamp": memory[3]
            }, indent=2, ensure_ascii=False))
