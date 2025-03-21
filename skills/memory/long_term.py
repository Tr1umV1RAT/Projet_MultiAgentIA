import sqlite3
from skills.base_skill import BaseSkill
from skills.communication.messages import Message  # <- Import ajouté ici clairement !

class LongTermMemory(BaseSkill):
    def __init__(self, db_name="memory.db"):
        super().__init__("LongTermMemory")
        self.connexion = sqlite3.connect(db_name)
        self.cursor = self.connexion.cursor()
        self.init_table()

    def init_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origine TEXT,
            destinataire TEXT,
            type_message TEXT,
            contenu TEXT,
            importance INTEGER,
            memoriser BOOLEAN,
            dialogue BOOLEAN,
            action TEXT,
            affichage_force BOOLEAN,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.connexion.commit()

    def save(self, message: Message):
        self.cursor.execute(
            "INSERT INTO memory (origine, destinataire, type_message, contenu, importance, memoriser, dialogue, action, affichage_force) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                message.origine,
                message.destinataire,
                message.type_message,
                message.contenu,
                message.importance,
                message.memoriser,
                message.dialogue,
                message.action,
                message.affichage_force
            )
        )
        self.connexion.commit()

    def recall(self, destinataire=None, type_message=None, limit=10):
        query = "SELECT * FROM memory WHERE 1=1"
        params = []
        if destinataire:
            query += " AND destinataire=?"
            params.append(destinataire)
        if type_message:
            query += " AND type_message=?"
            params.append(type_message)
        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()
