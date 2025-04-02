# config.py

class Config:
    # Paramètres de verbosité (mode debug global)
    verbose = True
    verbose_communication = True

    # Configuration du LLM
    LLM_PROVIDER = "ollama"
    LLM_MODEL = "mistral:latest"
    LLM_ENDPOINT = "http://localhost:11434"
    LLM_API_KEY = ""
    LLM_INJECTION_MODE = "direct"

    # Schéma de base pour les tables de messages
    MESSAGE_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            origine TEXT,
            destinataire TEXT,
            type_message TEXT,
            contenu TEXT,
            importance INTEGER,
            memoriser BOOLEAN,
            dialogue BOOLEAN,
            action TEXT,
            affichage_force BOOLEAN,
            version_finale BOOLEAN DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            conversation_id TEXT
        );
    """

    # Schéma pour la mémoire à long terme (si besoin séparé)
    MEMORY_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origine TEXT,
            destinataire TEXT,
            type_message TEXT,
            contenu TEXT,
            importance INTEGER,
            memoriser BOOLEAN,
            dialogue BOOLEAN,
            action TEXT,
            affichage_force BOOLEAN,
            version_finale BOOLEAN DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
