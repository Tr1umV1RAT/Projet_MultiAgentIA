from tools.base_tool import BaseTool
import requests

class LLMTool(BaseTool):
    def __init__(self, model: str, api_url: str, api_key: str = None):
        super().__init__(name="LLMTool", description="Outil générique pour interagir avec un LLM.")
        self.model = model
        self.api_url = api_url
        self.api_key = api_key

    def run(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.post(
            self.api_url,
            headers=headers,
            json={"model": self.model, "prompt": prompt}
        )
        response.raise_for_status()
        return response.json().get('text', '')
