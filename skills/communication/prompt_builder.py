# communication/prompt_builder.py

from typing import Optional
from skills.communication.messages import Message  # si besoin de typer plus tard

class PromptBuilder:
    @staticmethod
    def build(
        role,
        instruction: str,
        memory: Optional[str] = None,
        code: Optional[str] = None,
        feedback: Optional[str] = None,
        plan: Optional[str] = None,
        phase: Optional[str] = None
    ) -> str:
        """
        Construit dynamiquement un prompt contextuel à partir des éléments mémoire,
        feedback narratif, code existant et instruction utilisateur.
        """
        sections = []

        if memory:
            sections.append(f"\U0001f9e0 CONTEXTE MEMOIRE :\n{memory}")
        if plan:
            sections.append(f"\U0001f4c8 PLAN ACTUEL :\n{plan}")
        if code:
            sections.append(f"\U0001f4bb CODE EXISTANT :\n{code}")
        if feedback:
            sections.append(f"\u270d\ufe0f RETOURS NARRATIFS :\n{feedback}")
        if phase:
            sections.append(f"\U0001f504 PHASE DU ROUND : {phase}")

        sections.append(f"\U0001f3af INSTRUCTION :\n{instruction}")

        prompt_core = "\n\n".join(sections)
        return role.get_prompt(prompt_core)
