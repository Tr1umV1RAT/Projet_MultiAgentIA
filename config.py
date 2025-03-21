class Config:
    
    LLM_PROVIDER = "ollama"  # Nom du fournisseur LLM à utiliser
    LLM_MODEL = "mistral"    # Modèle spécifique du LLM
    verbose = True  # Active/Désactive les logs détaillés

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
        affichage_force BOOLEAN,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );"""
