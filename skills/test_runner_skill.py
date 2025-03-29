import os
import subprocess
from datetime import datetime

class SkillTestRunner:
    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "code")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def run_test_on_file(self, filepath: str) -> str:
        full_path = os.path.join(self.project_path, filepath)
        if not os.path.exists(full_path):
            return f"[SkillTestRunner] Erreur : le fichier {full_path} n'existe pas."

        try:
            result = subprocess.run(
                ["python", full_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                text=True
            )
            output = result.stdout.strip()
            errors = result.stderr.strip()
        except Exception as e:
            output = ""
            errors = str(e)

        report = f"""
==== TEST DU FICHIER : {filepath} ====

--- SORTIE STANDARD ---
{output if output else '[Aucune sortie]'}

--- ERREURS ---
{errors if errors else '[Aucune erreur]'}
"""

        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_result_{os.path.basename(filepath)}_{timestamp}.txt"
        result_path = os.path.join(self.project_path, filename)
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(report)

        if self.verbose:
            print(f"[SkillTestRunner] Rapport enregistré : {result_path}")

        if self.memory:
            self.memory.store_document(
                content=report,
                metadata={
                    "type": "test_result",
                    "tested_file": filepath,
                    "timestamp": timestamp
                }
            )

        return report
