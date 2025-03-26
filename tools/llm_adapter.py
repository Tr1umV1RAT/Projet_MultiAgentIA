# tools/llm_adapter.py
from config import Config
from tools.base_tool import BaseTool
import requests
try:
    import openai
except ImportError:
    openai = None

class LLMAdapterTool(BaseTool):
    def __init__(self, agent=None, model_name: str = None, temperature: float = 0.7):
        super().__init__("LLM")
        self.agent = agent
        self.model_name = model_name or Config.LLM_MODEL
        self.temperature = temperature

    def query(self, prompt):
        """Appelle le LLM configuré avec le prompt donné et retourne la réponse."""
        provider = Config.LLM_PROVIDER.lower()

        if provider == "ollama":
            endpoint = Config.LLM_ENDPOINT.rstrip("/") if Config.LLM_ENDPOINT else "http://localhost:11434"
            url = f"{endpoint}/api/generate"
            data = {"model": self.model_name, "prompt": prompt, "stream": False}
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", str(result))

        elif provider == "openai":
            if openai is None:
                raise ImportError("Le module openai n'est pas installé.")
            if Config.LLM_API_KEY:
                openai.api_key = Config.LLM_API_KEY
            if Config.LLM_ENDPOINT:
                openai.api_base = Config.LLM_ENDPOINT

            messages = []
            if "Question:" in prompt:
                idx = prompt.rfind("Question:")
                system_prompt = prompt[:idx].strip()
                user_prompt = prompt[idx+len("Question:"):].strip()
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": user_prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()

        else:
            raise ValueError(f"LLM_PROVIDER inconnu: {Config.LLM_PROVIDER}")
    def run(self, prompt):
            return self.query(prompt)