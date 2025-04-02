# skills/planning_skill.py

import os
from datetime import datetime

from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_interface import LLMInterface
class SkillPlanning(BaseSkill):
    name = "plan"

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
                sections.append("==== PLAN ACTUEL ====" +
                                f"\n{previous_plan['content']}\n")

        # Section : code existant
        if self.memory_codeur:
            validated_code = self.memory_codeur.search_documents({"type": "code", "status": "validated"})
            if validated_code:
                code_snippets = "\n\n".join([doc["content"] for doc in validated_code])
                sections.append("==== CODE EXISTANT ====" +
                                f"\n{code_snippets}\n")

        sections.append(f"==== OBJECTIF ACTUEL ====" + f"\n{objectif.strip()}\n")

        prompt = "\n\n".join(sections)

        if self.verbose:
            print("[SkillPlanning] Prompt de planification:\n", prompt)

        return self.agent.llm.query(prompt)

    def run(self, message: Message) -> Message:
        objectif = message.contenu.strip()
        plan = self.generate_plan(objectif)

        # Sauvegarde locale du plan
        filename = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(self.project_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(plan)

        if self.verbose:
            print(f"[SkillPlanning] Plan écrit dans {path}")

        return Message(
            origine=self.agent.name,
            destinataire=message.origine,
            contenu=plan,
            conversation_id=message.conversation_id,
            metadata={"type": "plan", "status": "draft"}
        )
