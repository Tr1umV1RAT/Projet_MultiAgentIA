# skills/coder_skill.py

import os
from datetime import datetime
from tools.llm_interface import LLMInterface
from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class SkillCoder(BaseSkill):
    name = "coder"

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
                    prompt_sections.append(f"Dernier brouillon de code :\n{last_draft['content']}\n")

        if context:
            prompt_sections.append(f"Contexte :\n{context}\n")

        prompt_sections.append(f"Instruction :\n{instruction}")

        final_prompt = "\n\n".join(prompt_sections)
        response = self.agent.llm.query(final_prompt)

        filename = f"{filename_hint}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        full_path = os.path.join(self.project_path, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(response)

        if self.verbose:
            print(f"[SkillCoder] Code écrit dans : {full_path}")

        return response

    def run(self, message: Message) -> Message:
        instruction = message.contenu
        context = message.metadata.get("context")
        first_call = message.metadata.get("first_call", True)

        generated_code = self.generate_code(
            instruction=instruction,
            context=context,
            first_call=first_call
        )

        return Message(
            origine=self.agent.name,
            destinataire=message.origine,
            contenu=generated_code,
            conversation_id=message.conversation_id,
            metadata={"type": "code", "status": "draft"}
        )
