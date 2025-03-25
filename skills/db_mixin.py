# skills/db_mixin.py
import sqlite3
from config import MEMORY_TABLE_SCHEMA

class PickleableDBMixin:
    def __getstate__(self):
        state = self.__dict__.copy()
        # Supprimer les objets non pickle-ables
        state.pop("connexion", None)
        state.pop("cursor", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.connexion = sqlite3.connect(self.db_name)
        self.cursor = self.connexion.cursor()
        self.init_schema(MEMORY_TABLE_SCHEMA)
