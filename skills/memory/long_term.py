import os
import sqlite3
import json
from datetime import datetime
from skills.communication.messages import Message

class LongTermMemory:
    def __init__(self, agent_id: str, base_path: str = "agent_memories", reuse: bool = False):
        """
        Initialise une mémoire longue pour un agent.
        - Si reuse=True, cherche une mémoire existante (agent_id_X).
        - Sinon, crée un nouveau dossier daté dans base_path.
        """
        self.agent_id = agent_id
        self.base_path = base_path

        if reuse:
            self.memory_path = self._find_latest_memory_dir()
            if not self.memory_path:
                print(f"[LongTermMemory] ❌ Aucune mémoire existante pour {agent_id}, création forcée.")
                self.memory_path = self._create_new_memory_dir()
        else:
            self.memory_path = self._create_new_memory_dir()

        self.db_path = os.path.join(self.memory_path, "long_term_memory.db")
        os.makedirs(self.memory_path, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

        print(f"[LongTermMemory] 📁 Mémoire {'existante' if reuse else 'nouvelle'} chargée : {self.memory_path}")

    def _create_new_memory_dir(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.base_path, f"{self.agent_id}_{timestamp}")

    def _find_latest_memory_dir(self):
        if not os.path.exists(self.base_path):
            return None
        candidates = sorted(
            [d for d in os.listdir(self.base_path) if d.startswith(self.agent_id)],
            reverse=True
        )
        if not candidates:
            return None
        return os.path.join(self.base_path, candidates[0])

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def store(self, message):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO memory (timestamp, role, content)
                VALUES (datetime('now'), ?, ?)
            ''', (getattr(message, "role", "unknown"), message.to_json()))
            self.conn.commit()
        except Exception as e:
            print(f"[LongTermMemory] ⚠️ Erreur d’enregistrement : {e}")

    def query(self, question: str, llm) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM memory ORDER BY id DESC LIMIT 50")
        results = [row[0] for row in cursor.fetchall()]
        joined = "\n".join(results)

        prompt = f"""Tu es une mémoire. On te donne des souvenirs, et une question.
Souvenirs :
{joined}

Question :
{question}

Réponds uniquement par les souvenirs pertinents, sans rien inventer."""

        try:
            if hasattr(llm, "query"):
                return llm.query(prompt)
            elif hasattr(llm, "ask"):
                message = llm.ask(prompt)
                return getattr(message, "contenu", str(message))
            elif callable(llm):
                return llm(prompt)
            else:
                raise ValueError("[LongTermMemory] LLM non compatible")
        except Exception as e:
            return f"[LongTermMemory] ⚠️ Erreur lors de l'interrogation du LLM : {e}"

    def prune(self, keep_last: int = 500):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            DELETE FROM memory
            WHERE id NOT IN (
                SELECT id FROM memory ORDER BY id DESC LIMIT {keep_last}
            )
        ''')
        self.conn.commit()

    def fetch(self, type_message=None, min_importance=2, limit=50, as_message=True):
        cursor = self.conn.cursor()
        query = "SELECT timestamp, role, content FROM memory WHERE 1=1"
        params = []

        if min_importance is not None:
            query += " AND (SELECT CAST(json_extract(content, '$.importance') AS INTEGER)) >= ?"
            params.append(min_importance)

        if type_message:
            query += " AND content LIKE ?"
            params.append(f"%\"type_message\": \"{type_message}\"%")

        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        try:
            cursor.execute(query, tuple(params))
            raw_results = cursor.fetchall()
        except sqlite3.OperationalError as e:
            if "malformed JSON" in str(e):
                print("[LongTermMemory] ⚠️ Base non conforme JSON, fallback brutal.")
                cursor.execute("SELECT timestamp, role, content FROM memory ORDER BY id DESC LIMIT ?", (limit,))
                raw_results = cursor.fetchall()
            else:
                raise

        results = []
        for ts, role, content in raw_results:
            try:
                obj = json.loads(content)
                parsed = Message.from_dict(obj) if as_message else obj
            except Exception as err:
                print(f"[LongTermMemory] ⚠️ Parsing erreur sur une entrée : {err}")
                parsed = content
            results.append({
                "timestamp": ts,
                "role": role,
                "content": parsed
            })
        return results
