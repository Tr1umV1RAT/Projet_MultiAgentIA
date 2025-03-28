# skills/coder/code_postprocessor.py

import os
import re
import uuid
from typing import Optional

from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from skills.memory.memory_manager import MemoryManager


class CodePostProcessorSkill(BaseSkill):
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose

    def handle_message(self, message: Message, agent=None) -> Message:
        agent = agent or self.agent

        if not message or not isinstance(message.contenu, str):
            raise ValueError(f"[{agent.name}] Message vide ou invalide reçu dans CodePostProcessorSkill.")

        code = self._extract_code(message.contenu)
        filename = self._extract_filename(message.contenu) or self._generate_filename()

        if self.verbose:
            print(f"[{agent.name}] [CODE-SKILL] Extraction fichier : {filename}")

        filepath = os.path.join(agent.project_path, filename)
        self._save_code_to_file(filepath, code)

        if self.verbose:
            print(f"[{agent.name}] [CODE-SKILL] Code sauvegardé dans {filepath}")

        db_skill = self._get_db_skill()
        if db_skill:
            db_skill.save_message(
                Message(
                    origine=agent.name,
                    destinataire="Archiviste",
                    type_message="code_sauvegardé",
                    contenu=f"Code sauvegardé sous {filename}",
                    meta={"filename": filename, "contenu_brut": code},
                    conversation_id=message.conversation_id or message.id
                )
            )

        return Message(
            origine=agent.name,
            destinataire=message.origine,
            type_message="confirmation",
            contenu=f"Code extrait et sauvegardé sous le nom : {filename}",
            meta={"filename": filename},
            conversation_id=message.conversation_id or message.id
        )

    def _extract_code(self, text: str) -> str:
        match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
        return match.group(1).strip() if match else text.strip()

    def _extract_filename(self, text: str) -> Optional[str]:
        match = re.search(r"# fichier: (.*?\.py)", text)
        return match.group(1).strip() if match else None

    def _generate_filename(self) -> str:
        return f"{uuid.uuid4().hex[:8]}.py"

    def _save_code_to_file(self, path: str, code: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

    def _get_db_skill(self):
        for skill in self.agent.skills:
            if hasattr(skill, "save_message"):
                return skill
        return None
