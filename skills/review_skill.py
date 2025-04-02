# skills/review_skill.py

import os
from datetime import datetime
from tools.llm_interface import LLMInterface
from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class SkillReview(BaseSkill):
    name = "review"

    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "reviews")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def run(self, message: Message) -> Message:
        if message.metadata.get("type") != "code":
            return Message(
                origine=self.agent.name,
                destinataire=message.origine,
                contenu="[SkillReview] Message ignoré (non code)",
                conversation_id=message.conversation_id,
                metadata={"type": "log", "status": "skipped"}
            )

        prompt = f"""
Tu es un Reviewer IA. Ton rôle est de relire le code suivant :

{message.contenu}

Ta tâche :
- Identifier les erreurs potentielles (syntaxe, logique, performance)
- Suggérer des améliorations claires et précises
- Indiquer si le code est fonctionnel ou non

Structure ta réponse en :\n\n1. Analyse\n2. Suggestions\n3. Verdict
"""

        feedback = self.agent.llm.query(prompt)

        # Sauvegarde dans fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"review_{timestamp}.md"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(feedback)

        if self.memory:
            msg = Message(
                origine=self.agent.name,
                destinataire="Archivage",
                contenu=feedback,
                metadata={
                    "type": "review",
                    "status": "draft",
                    "timestamp": timestamp
                }
            )
            self.memory.store_to_ltm(msg)

        return Message(
            origine=self.agent.name,
            destinataire=message.origine,
            contenu=feedback,
            conversation_id=message.conversation_id,
            metadata={"type": "review", "status": "draft"}
        )