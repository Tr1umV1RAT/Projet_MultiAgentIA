import os
import sqlite3
from datetime import datetime
from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class GlobalDBRegistry(BaseSkill):
    """
    Ce skill permet d'enregistrer dynamiquement des bases de données utilisées par des agents ou des équipes,
    avec description et catégorisation. Il utilise une base SQLite interne pour stocker les chemins et métadonnées.
    """

    def __init__(self, registry_path: str = "global_registry.db"):
        self.registry_path = registry_path
        self.connexion = sqlite3.connect(registry_path)
        self.cursor = self.connexion.cursor()
        self.init_table()

    def init_table(self):
        """Initialise la table d'index des bases si elle n'existe pas."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS databases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            db_name TEXT UNIQUE,
            db_path TEXT,
            agent_or_team TEXT,
            description TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.connexion.commit()

    def register_database(self, db_name: str, db_path: str, agent_or_team: str, description: str = ""):
        """Ajoute une nouvelle base au registre."""
        self.cursor.execute("""
        INSERT OR REPLACE INTO databases (db_name, db_path, agent_or_team, description)
        VALUES (?, ?, ?, ?)
        """, (db_name, db_path, agent_or_team, description))
        self.connexion.commit()

    def list_databases(self, filter_by_agent_or_team: str = None) -> list[dict]:
        """Retourne toutes les bases enregistrées, éventuellement filtrées."""
        if filter_by_agent_or_team:
            self.cursor.execute("""
            SELECT db_name, db_path, agent_or_team, description, date_created
            FROM databases
            WHERE agent_or_team = ?
            """, (filter_by_agent_or_team,))
        else:
            self.cursor.execute("""
            SELECT db_name, db_path, agent_or_team, description, date_created
            FROM databases
            """)
        rows = self.cursor.fetchall()
        return [
            {
                "db_name": name,
                "db_path": path,
                "agent_or_team": owner,
                "description": desc,
                "date_created": date
            } for name, path, owner, desc, date in rows
        ]

    def get_database_path(self, db_name: str) -> str | None:
        """Renvoie le chemin d'une base en fonction de son nom."""
        self.cursor.execute("SELECT db_path FROM databases WHERE db_name = ?", (db_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_database_reference(self, db_name: str):
        """Supprime l’entrée du registre (pas le fichier sur disque)."""
        self.cursor.execute("DELETE FROM databases WHERE db_name = ?", (db_name,))
        self.connexion.commit()

    def close(self):
        """Ferme la connexion proprement."""
        self.connexion.close()

    def execute(self, message: Message):
        """
        Implémentation vide de execute() pour respecter l'interface BaseSkill.
        """
        print(f"[GlobalDBRegistry] Reçu un message non traité : {message}")
