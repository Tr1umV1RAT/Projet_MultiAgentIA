# skills/memory/long_term.py

import sqlite3
import os
from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class LongTermMemory(BaseSkill):
    def __init__(self, db_name="memory.db", schema=None, description=None):
        super().__init__("LongTermMemory")
        self.db_name = db_name
        self.connexion = sqlite3.connect(db_name)
        self.cursor = self.connexion.cursor()
        if schema:
            self.init_table(schema)
        else:
            self.init_table()
        if description:
            # Enregistrer la DB dans le registre global si besoin
            from skills.db_management.global_registry import GlobalDBRegistry
            registry = GlobalDBRegistry()
            registry.register_database(
                db_name=db_name,
                db_path=os.path.abspath(db_name),
                agent_or_team="unknown",
                description=description
            )
    
    def init_table(self, schema=None):
        if schema:
            self.cursor.execute(schema)
        else:
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
                message.meta.get("type_message"),
                message.contenu,
                message.importance,
                message.meta.get("memoriser", True),
                message.dialogue,
                message.meta.get("action"),
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

    def close(self):
        self.connexion.close()

    def execute(self, message: Message):
        """
        Implémentation minimale pour satisfaire BaseSkill.
        Ici, on se contente de sauvegarder le message.
        """
        self.save(message)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Supprimer les objets non sérialisables
        if 'connexion' in state:
            del state['connexion']
        if 'cursor' in state:
            del state['cursor']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Rétablir la connexion SQLite après le chargement
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()
        self.init_table()
