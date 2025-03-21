import requests
from llm.base_llm import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"http://localhost:11400/generate",
            json={"model": self.model, "prompt": prompt}
        )
        return response.json().get('text', '')
