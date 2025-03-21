import requests
from tools.base_tool import BaseTool

class OllamaTool(BaseTool):
    def __init__(self, model="mistral"):
        super().__init__("OllamaTool")
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def run(self, query):
        data = {"model": self.model, "prompt": query, "stream": False}
        response = requests.post(self.url, json=data)
        response.raise_for_status()
        return response.json()['response']
