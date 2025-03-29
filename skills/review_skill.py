import os
from datetime import datetime

class SkillReview:
    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "reviews")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def review_code(self, code: str) -> str:
        prompt = f"""
Tu es un Reviewer IA. Ton rôle est de vérifier la qualité du code suivant :

{code}

Tu dois :
- Identifier les erreurs potentielles (syntaxe, logique, performance)
- Suggérer des améliorations claires et pratiques
- Indiquer si le code est valide ou non

Ta réponse doit être structurée, concise, et directement utile au Codeur.
"""

        feedback = self.agent.llm.query(prompt)

        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"review_{timestamp}.md"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(feedback)

        if self.verbose:
            print(f"[SkillReview] Commentaire enregistré dans : {filepath}")

        if self.memory:
            self.memory.store_document(
                content=feedback,
                metadata={
                    "type": "review",
                    "timestamp": timestamp
                }
            )

        return feedback
