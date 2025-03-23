# skills/db_management/db_management.py

import sqlite3
import os
from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from skills.db_management.global_registry import GlobalDBRegistry
from config import Config

class DBManagementSkill(BaseSkill):
    def __init__(self, db_name="default_memory.db", schema=None, overwrite=False, adapt_name_if_exists=True, connexion=None):
        super().__init__("DBManagement")
        self.db_name = db_name
        if connexion is None:
            self.connexion = sqlite3.connect(db_name)
            self.cursor = self.connexion.cursor()
            if not schema:
                schema = Config.MEMORY_TABLE_SCHEMA
            self.init_schema(schema)
            self.global_registry = GlobalDBRegistry()
            self.global_registry.register_database(
                db_name=self.db_name,
                db_path=os.path.abspath(self.db_name),
                agent_or_team="unknown",
                description=f"Base créée pour {self.db_name}"
            )
        else:
            # Utilisation d'une connexion déjà ouverte pour éviter la duplication de la DB
            self.connexion = connexion
            self.cursor = self.connexion.cursor()

    def init_schema(self, schema):
        self.cursor.execute(schema)
        self.connexion.commit()

    def save_message(self, message: Message):
        self.cursor.execute(
            """
            INSERT INTO memory (origine, destinataire, type_message, contenu, importance, memoriser, dialogue, action, affichage_force)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
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

    def recall_messages(self, destinataire=None, type_message=None, limit=10):
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
        # Implémentation simple : enregistre le message
        self.save_message(message)

    def __getstate__(self):
        state = self.__dict__.copy()
        if "connexion" in state:
            del state["connexion"]
        if "cursor" in state:
            del state["cursor"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()
        self.init_schema(Config.MEMORY_TABLE_SCHEMA)
