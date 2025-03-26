import os
import sqlite3
from datetime import datetime
import json
from .base_access_protocol import BaseAccessProtocol

class MemoryAccessProtocol(BaseAccessProtocol):
    """
    Protocole d'accès inter-agent à une mémoire longue.
    Gère :
    - L'autorisation (extensible)
    - La journalisation dans une base sqlite
    - L'accès aux souvenirs via fetch() de LongTermMemory
    """

    def __init__(self, requester: str, target_agent_name: str, log_db_path: str = "/mnt/data/memory_access_log.db"):
        self.requester = requester
        self.target = target_agent_name
        self.db_path = log_db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                requester TEXT,
                target_agent TEXT,
                action TEXT,
                meta TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def is_authorized(self, reason: str = "") -> bool:
        """
        À surcharger si besoin. Ici, tout est autorisé.
        """
        return True

    def log_access(self, action: str, meta: dict = None):
        """
        Enregistre un accès mémoire dans le journal.
        """
        meta_str = json.dumps(meta or {}, ensure_ascii=False)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO memory_access_log (timestamp, requester, target_agent, action, meta)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), self.requester, self.target, action, meta_str))
        conn.commit()
        conn.close()

    def read(self, long_term_memory, filtre: dict = None) -> list:
        """
        Lit les souvenirs d'un autre agent à travers son objet LongTermMemory.
        """
        if not self.is_authorized():
            raise PermissionError("Accès non autorisé à la mémoire de l'agent.")

        filtre = filtre or {}
        self.log_access("read", meta=filtre)

        return long_term_memory.fetch(
            type_message=filtre.get("type"),
            min_importance=filtre.get("min_importance", 2),
            limit=filtre.get("limit", 50)
        )

    def get_logs(self, limit: int = 100):
        """
        Récupère les derniers accès enregistrés.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, requester, target_agent, action, meta
            FROM memory_access_log
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "timestamp": row[0],
            "requester": row[1],
            "target": row[2],
            "action": row[3],
            "meta": json.loads(row[4])
        } for row in rows]
