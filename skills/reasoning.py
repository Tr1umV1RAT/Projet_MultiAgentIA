from skills.base_skill import BaseSkill
from tools.ollama_tool import OllamaTool

class Reasoning(BaseSkill):
    def __init__(self, name="Reasoning", model="mistral"):
        super().__init__(name)
        self.ollama = OllamaTool(model=model)

    def reflechir(self, prompt):
        return self.ollama.run(prompt)
