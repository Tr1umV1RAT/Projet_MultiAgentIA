# roles/base_role.py

class BaseRole:
    def __init__(
        self,
        name: str,
        objectif: str,
        contexte: str = "",
        instructions_specifiques: str = "",
        outils: list = None,
    ):
        self.name = name
        self.objectif = objectif.strip()
        self.contexte = contexte.strip()
        self.instructions_specifiques = instructions_specifiques.strip()
        self.outils = outils if outils is not None else []

    def get_prompt(self, message: str) -> str:
        """
        Génère un prompt contextuel pour le LLM, enrichi des éléments du rôle.

        :param message: Message à traiter (ex: tâche ou requête)
        :return: Prompt complet prêt à l’envoi
        """
        sections = [
            f"Rôle : {self.name}",
            f"Objectif : {self.objectif}",
        ]

        if self.contexte:
            sections.append(f"Contexte :\n{self.contexte}")
        if self.instructions_specifiques:
            sections.append(f"Instructions spécifiques :\n{self.instructions_specifiques}")

        sections.append(f"Tâche reçue :\n{message}")

        return "\n\n".join(sections)

    def get_outils(self):
        return self.outils

    def __repr__(self):
        return f"<Role {self.name}>"
