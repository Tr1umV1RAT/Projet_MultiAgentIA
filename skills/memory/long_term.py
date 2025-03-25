# skills/memory/long_term.py
import sqlite3
from config import MEMORY_TABLE_SCHEMA
from skills.db_mixin import PickleableDBMixin
from skills.communication.messages import Message  # Assure-toi que Message est correctement défini

class LongTermMemory(PickleableDBMixin):
    def __init__(self, db_name="long_term_memory.db"):
        self.db_name = db_name
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()
        self.init_schema(MEMORY_TABLE_SCHEMA)

    def init_schema(self, schema):
        self.cursor.execute(schema)
        self.connexion.commit()
        
    def save(self, message: Message):
        query = (
            "INSERT INTO memory (origine, destinataire, type_message, contenu, importance, memoriser, dialogue, action, affichage_force, version_finale) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        self.cursor.execute(query, (
            message.origine,
            message.destinataire,
            message.type_message,
            message.contenu,
            message.importance,
            message.memoriser,
            message.dialogue,
            message.action,
            message.affichage_force,
            int(message.version_finale)
        ))
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
        Implémentation minimale pour satisfaire l'interface de BaseSkill.
        Ici, on se contente de sauvegarder le message.
        """
        self.save(message)