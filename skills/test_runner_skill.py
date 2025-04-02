# skills/test_runner_skill.py
import os
import tempfile
import subprocess

from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class SkillTestRunner(BaseSkill):
    name = "test_runner"

    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose

    def run(self, message: Message) -> Message:
        code = message.contenu

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_code.py")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                result = subprocess.run(
                    ["python", filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout.strip()
                error = result.stderr.strip()

                if result.returncode == 0:
                    status = "passed"
                else:
                    status = "failed"
            except Exception as e:
                output = ""
                error = str(e)
                status = "error"

        if self.verbose:
            print(f"[TestRunner] Résultat du test : {status}")
            if output:
                print("[stdout]", output)
            if error:
                print("[stderr]", error)

        return Message(
            origine=self.agent.name,
            destinataire=message.origine,
            contenu=f"Résultat du test : {status}\n\nSTDOUT:\n{output}\n\nSTDERR:\n{error}",
            metadata={
                "type": "test_result",
                "status": status,
                "stdout": output,
                "stderr": error
            }
        )