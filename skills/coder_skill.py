import os
from datetime import datetime

class SkillCoder:
    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = project_path
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def generate_code(self, instruction: str, context: str = None, filename_hint: str = "code_block", first_call: bool = True) -> str:
        prompt_sections = []

        if self.memory:
            if first_call:
                validated_snippets = self.memory.search_documents({"type": "code", "status": "validated"})
                if validated_snippets:
                    code_valides = "\n\n".join([doc["content"] for doc in validated_snippets])
                    prompt_sections.append(f"Code déjà validé :\n{code_valides}\n\nIMPORTANT : Ne le réécris pas.")
            else:
                last_draft = self.memory.get_last_document({"type": "code", "status": "draft"})
                if last_draft:
                    prompt_sections.append(f"Dernier code à corriger :\n{last_draft['content']}\n")

                comments = self.memory.search_documents({"type": "review"})
                if comments:
                    commentaires = "\n\n".join([doc["content"] for doc in comments])
                    prompt_sections.append(f"Commentaires à intégrer :\n{commentaires}\n")

        # Ajout de l'instruction principale
        prompt_sections.append(f"Instruction actuelle :\n{instruction}")

        # Génération du prompt complet
        if hasattr(self.agent, "role") and self.agent.role and hasattr(self.agent.role, "get_prompt"):
            full_instruction = "\n\n".join(prompt_sections)
            full_prompt = self.agent.role.get_prompt(full_instruction)
        else:
            full_prompt = "\n\n".join(["Tu es un assistant de codage. Voici le contexte :"] + prompt_sections)

        # Interrogation du LLM
        code = self.agent.llm.query(full_prompt)

        # Sauvegarde fichier brut
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_hint}_{timestamp}.py"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        if self.verbose:
            print(f"[SkillCoder] Code généré sauvegardé dans : {filepath}")

        # Enregistrement mémoire
        if self.memory:
            self.memory.store_document(
                content=code,
                metadata={
                    "type": "code",
                    "filename": filename,
                    "instruction": instruction,
                    "status": "draft",
                    "timestamp": timestamp
                }
            )

        return code
