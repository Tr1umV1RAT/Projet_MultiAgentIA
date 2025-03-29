import os
from datetime import datetime

class SkillPlanning:
    def __init__(self, agent, project_path="project_outputs", memory=None, memory_codeur=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "plans")
        self.memory = memory
        self.memory_codeur = memory_codeur
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def generate_plan(self, objectif: str) -> str:
        sections = []

        # Section : plan précédent
        if self.memory:
            previous_plan = self.memory.get_last_document({"type": "plan"})
            if previous_plan:
                sections.append(f"==== PLAN ACTUEL ===="
                                f"\n{previous_plan['content']}\n")

        # Section : code existant
        if self.memory_codeur:
            validated_code = self.memory_codeur.search_documents({"type": "code", "status": "validated"})
            if validated_code:
                all_snippets = "\n\n".join([doc["content"] for doc in validated_code])
                sections.append(f"==== CODE DEJA IMPLEMENTE ===="
                                f"\n{all_snippets}\n")

        # Objectif actuel
        sections.append(f"==== OBJECTIF ===="
                        f"\n{objectif}\n")

        # Consigne finale
        sections.append("""
==== CONSIGNE ====
Sur la base de ce plan et de ce code, indique ce qu’il reste à faire. 
Donne une instruction claire au Codeur pour la prochaine étape, sans redondance ni ambiguïté. Sois précis, technique, et évite les reformulations vagues.
""")

        full_prompt = "\n\n".join(sections)

        if hasattr(self.agent, "role") and self.agent.role and hasattr(self.agent.role, "get_prompt"):
            prompt = self.agent.role.get_prompt(full_prompt)
        else:
            prompt = f"Tu es un planificateur logiciel. Voici le contexte :\n\n{full_prompt}"

        plan = self.agent.llm.query(prompt)

        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plan_{timestamp}.md"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(plan)

        if self.verbose:
            print(f"[SkillPlanning] Plan enregistré dans : {filepath}")

        if self.memory:
            self.memory.store_document(
                content=plan,
                metadata={
                    "type": "plan",
                    "objectif": objectif,
                    "timestamp": timestamp
                }
            )

        return plan
