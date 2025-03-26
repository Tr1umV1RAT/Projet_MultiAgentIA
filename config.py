
# Paramètre global pour contrôler l'affichage des messages (mode debug/verbose)
VERBOSE_COMMUNICATION = True

# Valeur par défaut pour l'attribut affichage_force des messages
DEFAULT_AFFICHAGE_FORCE = True
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
        version_finale BOOLEAN DEFAULT 0,  -- 0 = temporaire, 1 = définitive
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

class Config:
    VERBOSE_COMMUNICATION = True
    DEFAULT_AFFICHAGE_FORCE = True
    LLM_PROVIDER = "ollama"       # Nom du fournisseur LLM à utiliser (ex: 'ollama', 'openai')
    LLM_MODEL = "mistral:latest"         # Modèle spécifique du LLM (ex: 'llama2', 'codellama', 'gpt-4')
    LLM_ENDPOINT = "http://localhost:11434"  # Endpoint du LLM (ex: 'http://localhost:11434' pour Ollama)
    LLM_API_KEY = ""              # Jeton/clé API si requis (par ex. pour OpenAI)
    LLM_INJECTION_MODE = "direct" # Mode d'injection des outils LLM : 'role' ou 'direct'

    verbose = True                # Active/Désactive les logs détaillés
    MESSAGE_FIELDS = [
        "id", "origine", "destinataire", "type_message", "contenu",
        "importance", "memoriser", "dialogue", "action", "affichage_force",
        "version_finale", "date", "meta", "conversation_id"
    ]

    MESSAGE_TABLE_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS messages (
        {', '.join([
            'id TEXT PRIMARY KEY',
            'origine TEXT',
            'destinataire TEXT',
            'type_message TEXT',
            'contenu TEXT',
            'importance INTEGER',
            'memoriser BOOLEAN',
            'dialogue BOOLEAN',
            'action TEXT',
            'affichage_force BOOLEAN',
            'version_finale BOOLEAN',
            'date TEXT',
            'meta TEXT',
            'conversation_id TEXT'
        ])}
    );
    """