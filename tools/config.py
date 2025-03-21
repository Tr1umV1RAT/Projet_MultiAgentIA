import ollama

class Config:
    DEBUG_MODE = True
    LLM_MODEL = "mistral-nemo"


    MEMORY = {}  # Stockage centralisé de la mémoire partagée

    @staticmethod
    def query_llm(prompt):
        """Effectue une requête au LLM via Ollama"""
        response = ollama.chat(model=Config.LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]


 
    @staticmethod
    def debug_log(message: str):
        """Affiche les logs uniquement si DEBUG_MODE est activé."""
        if Config.DEBUG_MODE:
            print(message)