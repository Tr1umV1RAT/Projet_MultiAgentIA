import requests
from tools.base_tool import BaseTool

class WebSearchTool(BaseTool):
    def __init__(self, name="WebSearch", model="mistral"):
        super().__init__(name)
        self.url = "http://localhost:11434/api/generate"
        self.model = model
        self.name = name

    def run(self, query):
        import requests
        data = {
            "model": self.model,
            "prompt": f"Fais un résumé court sur : {query}",
            "stream": False
        }
        try:
            response = requests.post("http://localhost:11434/api/generate", json=data)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.RequestException as e:
            return f"Erreur lors de la recherche web : {e}"
