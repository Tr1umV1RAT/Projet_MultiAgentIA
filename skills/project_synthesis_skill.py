import os
from datetime import datetime

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
            documents += self.memory.search_documents({"type": "code"})
            documents += self.memory.search_documents({"type": "review"})
            documents += self.memory.search_documents({"type": "narrative"})
            documents += self.memory.search_documents({"type": "plan"})

        # Tri par date si possible
        documents.sort(key=lambda x: x.get("metadata", {}).get("timestamp", ""))

        corpus = "\n\n====\n\n".join(doc["content"] for doc in documents if "content" in doc)

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
            self.memory.store_document(
                content=synthese,
                metadata={
                    "type": "synthese",
                    "timestamp": timestamp
                }
            )

        return synthese
