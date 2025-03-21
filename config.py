
# Paramètre global pour contrôler l'affichage des messages (mode debug/verbose)
VERBOSE_COMMUNICATION = False

# Valeur par défaut pour l'attribut affichage_force des messages
DEFAULT_AFFICHAGE_FORCE = False
class Config:
    
    LLM_PROVIDER = "ollama"       # Nom du fournisseur LLM à utiliser (ex: 'ollama', 'openai')
    LLM_MODEL = "mistral"         # Modèle spécifique du LLM (ex: 'llama2', 'codellama', 'gpt-4')
    LLM_ENDPOINT = "http://localhost:11434"  # Endpoint du LLM (ex: 'http://localhost:11434' pour Ollama)
    LLM_API_KEY = ""              # Jeton/clé API si requis (par ex. pour OpenAI)
    LLM_INJECTION_MODE = "direct" # Mode d'injection des outils LLM : 'role' ou 'direct'

    verbose = True                # Active/Désactive les logs détaillés
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
