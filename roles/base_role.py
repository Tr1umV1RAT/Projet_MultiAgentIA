class BaseRole:
    def __init__(self, nom_role, objectif, contexte, outils=None, instructions_specifiques=None):
        self.nom_role = nom_role
        self.objectif = objectif
        self.contexte = contexte
        self.outils = outils if outils else []
        self.instructions_specifiques = instructions_specifiques

    def generer_prompt(self, message):
        prompt = f"{self.contexte}\n\nObjectif : {self.objectif}\n\n"
        if self.instructions_specifiques:
            prompt += f"Instructions spécifiques : {self.instructions_specifiques}\n"
        prompt += f"\nQuestion: {message}\n"
        return prompt
