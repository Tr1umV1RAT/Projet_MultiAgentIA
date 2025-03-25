# skills/ollama_adapter.py
from config import Config
from tools.base_tool import BaseTool
import requests
try:
    import openai
except ImportError:
    openai = None

class LLMAdapterTool(BaseTool):
    def __init__(self):
        super().__init__("LLM")

    def run(self, prompt):
        """Appelle le LLM configuré avec le prompt donné et retourne la réponse."""
        provider = Config.LLM_PROVIDER.lower()
        if provider == "ollama":
            # Appel de l'API Ollama locale
            endpoint = Config.LLM_ENDPOINT.rstrip("/") if Config.LLM_ENDPOINT else "http://localhost:11434"
            url = f"{endpoint}/api/generate"
            data = {"model": Config.LLM_MODEL, "prompt": prompt, "stream": False}
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            # On retourne la réponse textuelle du modèle
            if isinstance(result, dict) and "response" in result:
                return result["response"]
            return str(result)
        elif provider == "openai":
            # Appel de l'API OpenAI (ChatCompletion)
            if openai is None:
                raise ImportError("Le module openai n'est pas installé.")
            if Config.LLM_API_KEY:
                openai.api_key = Config.LLM_API_KEY
            if Config.LLM_ENDPOINT:
                openai.api_base = Config.LLM_ENDPOINT
            model_name = Config.LLM_MODEL
            prompt_text = prompt
            # Préparation des messages pour l'API ChatCompletion
            messages = []
            if "Question:" in prompt_text:
                idx = prompt_text.rfind("Question:")
                system_content = prompt_text[:idx].strip()
                user_question = prompt_text[idx+len("Question:"):].strip()
                if system_content:
                    messages.append({"role": "system", "content": system_content})
                messages.append({"role": "user", "content": user_question})
            else:
                messages.append({"role": "user", "content": prompt_text})
            response = openai.ChatCompletion.create(model=model_name, messages=messages)
            return response.choices[0].message.content.strip()
        else:
            raise ValueError(f"LLM_PROVIDER inconnu: {Config.LLM_PROVIDER}")
