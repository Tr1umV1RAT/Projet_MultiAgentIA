# roles/base_role.py

class BaseRole:
    def __init__(self, name: str, prompt: str = "", description: str = None):
        self.name = name
        self.prompt = prompt
        self.description = description

    def get_prompt(self, contenu: str) -> str:
        return f"{self.prompt}\n\n{contenu}"