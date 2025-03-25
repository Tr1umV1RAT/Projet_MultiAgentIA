# skills/db_management/db_management.py
import sqlite3
import json
from typing import Optional, List, Any, Dict, Union
from datetime import datetime

from skills.communication.messages import Message
from config import Config

class DBManagementSkill:
    def __init__(self, db_name: str = "agent_data.db", table: str = "generic", verbose: bool = False):
        self.db_name = db_name
        self.table = table
        self.verbose = verbose
        self.schema = Config.MESSAGE_TABLE_SCHEMA
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()

    def init_schema(self, schema: str):
        self.schema = schema
        self.cursor.execute(schema.replace("messages", self.table))
        self.connexion.commit()

    def switch_table(self, table_name: str):
        self.table = table_name

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
        self.init_schema(self.schema)

    def save(self, data: Union[Dict[str, Any], Message]):
        if isinstance(data, Message):
            return self.save_message(data)
        fields = list(data.keys())
        values = list(data.values())
        placeholders = ", ".join("?" for _ in fields)
        query = f"INSERT OR REPLACE INTO {self.table} ({', '.join(fields)}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connexion.commit()
        if self.verbose:
            print(f"[DBSkill] Données sauvegardées dans {self.table} : {fields}")

    def save_message(self, message: Message):
        data = message.to_dict()
        data["meta"] = json.dumps(message.meta)
        values = [data[k] for k in Config.MESSAGE_FIELDS]
        placeholders = ", ".join("?" for _ in Config.MESSAGE_FIELDS)
        query = f"INSERT OR REPLACE INTO {self.table} ({', '.join(Config.MESSAGE_FIELDS)}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connexion.commit()
        if self.verbose:
            print(f"[DBSkill] Message sauvegardé dans {self.table} : {message}")

    def get_messages(self, where_clause: Optional[str] = None, params: tuple = (), limit: int = 10) -> List[Message]:
        query = f"SELECT * FROM {self.table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        query += f" ORDER BY date DESC LIMIT {limit}"
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [self._row_to_message(row) for row in rows]

    def _row_to_message(self, row) -> Message:
        fields = Config.MESSAGE_FIELDS
        data = dict(zip(fields, row))
        data["meta"] = json.loads(data["meta"])
        data["date"] = datetime.fromisoformat(data["date"])
        return Message(**data)

    def execute(self, message: Message):
        self.save(message)

    def close(self):
        self.connexion.close()
