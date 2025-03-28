from skills.base_skill import BaseSkill
from tools.llm_interface import LLMInterface

class CoderSkill(BaseSkill):
    def __init__(self, llm: LLMInterface, verbose=False):
        self.llm = llm
        self.verbose = verbose

    def generate_code(self, prompt):
        full_prompt = f"Tu es un agent programmeur expert. Ta tâche : {prompt}\n\nCode :"
        return self.llm.query(full_prompt)
