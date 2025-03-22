import sqlite3
import os
from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from skills.db_management.global_registry import GlobalDBRegistry
from config import Config

class DBManagementSkill(BaseSkill):
    def __init__(self, db_name="default_memory.db", schema=None, overwrite=False, adapt_name_if_exists=True):
        super().__init__("DBManagement")
        self.db_name = self._prepare_db_name(db_name, overwrite, adapt_name_if_exists)
        self.connexion = sqlite3.connect(self.db_name)
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

    def _prepare_db_name(self, db_name, overwrite, adapt_name_if_exists):
        base, ext = os.path.splitext(db_name)
        if os.path.exists(db_name):
            if overwrite:
                os.remove(db_name)
                print(f"⚠️ Base existante {db_name} supprimée explicitement.")
            elif adapt_name_if_exists:
                compteur = 1
                nouveau_nom = f"{base}_{compteur}{ext}"
                while os.path.exists(nouveau_nom):
                    compteur += 1
                    nouveau_nom = f"{base}_{compteur}{ext}"
                db_name = nouveau_nom
                print(f"ℹ️ Nom adapté automatiquement pour éviter conflit : {db_name}")
            else:
                print(f"ℹ️ Utilisation explicite de la base existante : {db_name}")
        return db_name

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
                message.expediteur,
                message.destinataire,
                message.meta.get("type_message"),
                message.contenu,
                message.meta.get("importance", 0),
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
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, message: Message):
        """
        Méthode requise par BaseSkill. Par défaut, elle enregistre le message.
        Elle pourrait être étendue à d'autres actions via message.meta['action'].
        """
        action = message.meta.get("action", "save")
        if action == "save":
            self.save_message(message)
        elif action == "recall":
            return self.recall_messages(
                destinataire=message.destinataire,
                type_message=message.meta.get("type_message")
            )
        else:
            print(f"⚠️ Action inconnue '{action}' pour DBManagementSkill")

    def close(self):
        self.connexion.close()
