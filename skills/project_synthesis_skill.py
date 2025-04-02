import os
from datetime import datetime
from skills.communication.messages import Message
from skills.memory.memory_manager import MemoryManager
from skills.communication.communication import Communication
from tools.llm_interface import LLMInterface

class SkillProjectSynthesis:
    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "syntheses")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def generate_synthesis(self) -> str:
        # Extraction brute des documents pertinents
        documents = []
        if self.memory:
            recent = self.memory.ltm.retrieve(query={}, max_results=50)

            documents = [msg for msg in recent if msg.metadata.get("type") in {"code", "review", "narration", "plan"}]

        # Tri par date si possible
        documents.sort(key=lambda x: x.metadata.get("timestamp", ""))

        corpus = "\n\n====\n\n".join(msg.contenu for msg in documents if hasattr(msg, "contenu"))

        prompt = f"""
Tu es un assistant IA chargé de rédiger une synthèse claire et exhaustive de l'état d'avancement d'un projet logiciel piloté par une équipe d'agents IA.

Voici les documents disponibles :
{corpus}

Résume de manière structurée :
- Ce qui a été fait (code validé, quêtes définies, modules créés...)
- Ce qui a été corrigé ou amélioré (par le reviewer)
- Ce qui reste à faire (prochaines étapes du plan, objectifs narratifs, code manquant)

Ta synthèse doit être exploitable par un humain ou par un ProjectManager IA pour orienter les prochaines actions.
"""

        synthese = self.agent.llm.query(prompt)

        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"synthese_{timestamp}.md"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(synthese)

        if self.verbose:
            print(f"[SkillProjectSynthesis] Synthèse enregistrée dans : {filepath}")

        if self.memory:
            from skills.communication.messages import Message
            self.memory.store_to_ltm(
                Message(
                    origine=self.agent.name,
                    destinataire="Archivage",
                    contenu=synthese,
                    metadata={"type": "synthese", "timestamp": timestamp}
                )
            )

        return synthese