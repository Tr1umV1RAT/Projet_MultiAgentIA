import sqlite3, os

class GlobalDBRegistry:
    def __init__(self, registry_path="global_db_registry.db"):
        self.connexion = sqlite3.connect(registry_path)
        self.cursor = self.connexion.cursor()
        self.init_table()

    def init_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS databases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            db_name TEXT UNIQUE,
            agent_or_team TEXT,
            description TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        self.connexion.commit()

    def register_db(self, db_name, description=""):
        self.cursor.execute(
            "INSERT OR IGNORE INTO databases (db_name, description) VALUES (?, ?)",
            (db_name, description)
        )
        self.connexion.commit()

    def list_dbs(self):
        return self.cursor.execute("SELECT * FROM databases ORDER BY date_created DESC").fetchall()

    def close(self):
        self.connexion.close()

