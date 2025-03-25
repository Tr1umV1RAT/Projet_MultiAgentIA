# skills/memory/long_term.py

import sqlite3
import json
from datetime import datetime
from typing import Optional, List

from config import Config
from skills.communication.messages import Message

class LongTermMemory:
    def __init__(self, db_path="long_term_memory.db", table_name="memory", verbose=False):
        self.db_path = db_path
        self.table_name = table_name
        self.verbose = verbose
        self.schema = Config.MESSAGE_TABLE_SCHEMA
        self.connexion = sqlite3.connect(self.db_path)
        self.cursor = self.connexion.cursor()
        self._init_schema()

    def _init_schema(self):
        self.cursor.execute(self.schema.replace("messages", self.table_name))
        self.connexion.commit()

    def __getstate__(self):
        state = self.__dict__.copy()
        if "connexion" in state:
            del state["connexion"]
        if "cursor" in state:
            del state["cursor"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.connexion = sqlite3.connect(self.db_path)
        self.cursor = self.connexion.cursor()
        self._init_schema()

    def save(self, message: Message):
        if not message.is_valid():
            raise ValueError("Message invalide : origine, destinataire et contenu requis.")
        data = message.to_dict()
        data["meta"] = json.dumps(message.meta)

        fields = Config.MESSAGE_FIELDS
        values = [data[k] for k in fields]
        placeholders = ", ".join("?" for _ in fields)
        query = f"INSERT OR REPLACE INTO {self.table_name} ({', '.join(fields)}) VALUES ({placeholders})"

        self.cursor.execute(query, values)
        self.connexion.commit()

        if self.verbose:
            print(f"[LongTermMemory] Message sauvegardé : {message}")

    def recall(self, destinataire: Optional[str] = None, type_message: Optional[str] = None, limit: int = 10) -> List[Message]:
        clause = []
        params = []

        if destinataire:
            clause.append("destinataire = ?")
            params.append(destinataire)
        if type_message:
            clause.append("type_message = ?")
            params.append(type_message)

        where = f"WHERE {' AND '.join(clause)}" if clause else ""
        query = f"SELECT * FROM {self.table_name} {where} ORDER BY date DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [self._row_to_message(row) for row in rows]

    def get_by_conversation(self, conversation_id: str) -> List[Message]:
        query = f"SELECT * FROM {self.table_name} WHERE conversation_id = ? ORDER BY date ASC"
        self.cursor.execute(query, (conversation_id,))
        rows = self.cursor.fetchall()
        return [self._row_to_message(row) for row in rows]

    def get_by_type(self, destinataire: str, type_message: str, limit: int = 10) -> List[Message]:
        return self.recall(destinataire=destinataire, type_message=type_message, limit=limit)

    def _row_to_message(self, row) -> Message:
        fields = Config.MESSAGE_FIELDS
        data = dict(zip(fields, row))
        data["meta"] = json.loads(data["meta"])
        data["date"] = datetime.fromisoformat(data["date"])
        return Message(**data)

    def count(self) -> int:
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.cursor.fetchone()[0]

    def close(self):
        self.connexion.close()

