# skills/db_management/db_management.py
import sqlite3
from config import MEMORY_TABLE_SCHEMA
from skills.db_mixin import PickleableDBMixin
from skills.communication.messages import Message

class DBManagementSkill(PickleableDBMixin):
    def __init__(self, db_name="agent_messages.db", verbose=False, agent=None):
        self.db_name = db_name
        self.verbose = verbose
        self.agent = agent  # Optionnel : si le skill doit connaître l'agent
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()
        self.init_schema(MEMORY_TABLE_SCHEMA)

    def init_schema(self, schema):
        self.cursor.execute(schema)
        self.connexion.commit()

    def save_message(self, message: Message):
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
        if self.verbose:
            print(f"Message sauvegardé : {message}")

    def get_messages(self, limit=10):
        query = "SELECT * FROM memory ORDER BY date DESC LIMIT ?"
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.connexion.close()

    def execute(self, message: Message):
        """
        Implémentation minimale pour satisfaire l'interface de BaseSkill.
        Ici, on se contente de sauvegarder le message.
        """
        self.save_message(message)

