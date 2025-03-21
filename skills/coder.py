from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class CoderSkill(BaseSkill):
    def __init__(self):
        super().__init__("Coder")

    def generer_code(self, demande: str) -> str:
        # Pour le moment, simple invocation du modèle LLM
        prompt = f"Tu es un expert en programmation.\n\nÉcris du code pour : {demande}\n\n" \
                 "Utilise les bonnes pratiques en programmation (commentaires, clarté, modularité)."
        
        code = self.llm.generer(prompt)
        return code
