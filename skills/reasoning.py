from skills.base_skill import BaseSkill
from tools.llm_adapter import LLMAdapterTool

class Reasoning(BaseSkill):
    def __init__(self, name="Reasoning"):
        super().__init__(name)
        # Initialise un outil LLMAdapterTool pour centraliser les appels au LLM
        self.llm_tool = LLMAdapterTool()

    def reflechir(self, prompt):
        return self.llm_tool.run(prompt)