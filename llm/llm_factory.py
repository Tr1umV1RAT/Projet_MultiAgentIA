from config import Config
from llm.ollama_llm import OllamaLLM
# Importer d'autres LLM si nécessaire

def get_llm_instance():
    if Config.LLM_PROVIDER == "ollama":
        return OllamaLLM(model=Config.LLM_MODEL)
    # Ajouter d'autres conditions pour différents LLM
    else:
        raise ValueError(f"LLM provider '{Config.LLM_PROVIDER}' is not supported.")
