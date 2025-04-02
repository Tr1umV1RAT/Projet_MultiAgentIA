# skills/narrative_skill.py

import os
from datetime import datetime
from skills.memory.memory_manager import MemoryManager
from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_interface import LLMInterface
class SkillNarrative(BaseSkill):
    name = "narrate"

    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "narration")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def run(self, message: Message) -> Message:
        instruction = message.contenu
        type_msg = message.metadata.get("type", "general")

        if type_msg == "code":
            prompt = f"""
Tu es un concepteur narratif IA. Voici un extrait de code produit par un codeur :

{instruction}

Ta tâche :
- Vérifie que les noms de variables, classes, fonctions soient cohérents avec un univers narratif immersif
- Propose des améliorations ou un style plus adapté
- Ne modifie pas la logique fonctionnelle, uniquement le contexte narratif
"""
        else:
            prompt = f"""
Tu es un narrateur IA. Génère une proposition de scénario, d'univers ou de monde immersif à partir de l'instruction suivante :

{instruction}

Inclue si possible :
- Un titre
- Une courte description du monde
- Quelques éléments narratifs clés (personnages, factions, enjeux)
"""

        feedback = self.agent.llm.query(prompt)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"narrative_{type_msg}_{timestamp}.md"
        path = os.path.join(self.project_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(feedback)

        if self.memory:
            msg = Message(
                origine=self.agent.name,
                destinataire="Archivage",
                contenu=feedback,
                metadata={
                    "type": "narration",
                    "subtype": type_msg,
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
            metadata={"type": "narration", "subtype": type_msg, "status": "draft"}
        )
