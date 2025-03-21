class BaseRole:
    def __init__(self, nom_role, objectif, contexte, instructions_specifiques, outils=None):
        """
        Initialise un rôle d'agent.
        
        :param nom_role: Nom du rôle (ex: 'Scientifique')
        :param objectif: Objectif du rôle (ex: 'Défendre les données scientifiques...')
        :param contexte: Contexte ou background à inclure dans le prompt.
        :param instructions_specifiques: Instructions supplémentaires pour guider le comportement.
        :param outils: Liste d'outils disponibles pour ce rôle (optionnel).
        """
        self.nom_role = nom_role
        self.objectif = objectif
        self.contexte = contexte
        self.instructions_specifiques = instructions_specifiques
        self.outils = outils if outils is not None else []

    def generer_prompt(self, message: str) -> str:
        """
        Génère un prompt enrichi en combinant le contexte, l'objectif et les instructions spécifiques
        du rôle avec le message de base.
        
        :param message: Le message ou la consigne initiale.
        :return: Le prompt enrichi à envoyer au LLM.
        """
        prompt = (
            f"Role: {self.nom_role}\n"
            f"Contexte: {self.contexte}\n"
            f"Objectif: {self.objectif}\n"
            f"Instructions: {self.instructions_specifiques}\n"
            f"Message: {message}\n"
        )
        return prompt
