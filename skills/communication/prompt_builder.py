# communication/prompt_builder.py

# skills/communication/prompt_builder.py

# Aucun import externe requis ici car tout est manipulé par concaténation texte

class PromptBuilder:
    @staticmethod
    def build(role=None, instruction=None, memory=None, phase=None, **kwargs):
        """
        Génère un prompt structuré à partir d'un rôle, d'une instruction et de divers éléments de contexte.
        """
        prompt_parts = []

        if role and hasattr(role, "system_prompt"):
            prompt_parts.append(f"🧠 RÔLE :\n{role.system_prompt.strip()}\n")

        if memory:
            prompt_parts.append(f"📚 MÉMOIRE :\n{memory.strip()}\n")

        if phase:
            prompt_parts.append(f"🔄 PHASE : {phase.strip()}\n")

        if instruction:
            prompt_parts.append(f"🎯 INSTRUCTION :\n{instruction.strip()}\n")

        # Ajout dynamique des éléments contextuels supplémentaires (code, review, plan, etc.)
        for key, value in kwargs.items():
            if value:
                title = key.upper().replace("_", " ")
                prompt_parts.append(f"🔹 {title} :\n{value.strip()}\n")

        return "\n".join(prompt_parts).strip()