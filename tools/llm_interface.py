import requests
import json
import ollama 

class LLMInterface:
    def __init__(self, model="ollama", agent=None, verbose=False, host="localhost", port=11434):
        self.model = model
        self.agent = agent
        self.verbose = verbose
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"

    def query(self, prompt: str, context=None, options=None) -> str:
        if self.model == "ollama":
            return self.query_ollama(prompt, context, options)
        raise ValueError(f"Modèle LLM inconnu : {self.model}")

    def query_ollama(self, prompt: str, context=None, options=None) -> str:
        url = f"{self.base_url}/api/generate"
        data = {
            "model": "mistral",  # ou paramétrable
            "prompt": prompt,
            "stream": False,
            "context": context,
            "options": options or {},
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("response", "")
        except requests.RequestException as e:
            if self.verbose:
                print(f"[Erreur Ollama] {e}")
            return "[Erreur Ollama]"
