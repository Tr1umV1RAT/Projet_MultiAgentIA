from skills.communication.communication import Communication
from skills.communication.message import Message

class BaseTeam:
    """Classe de base orchestrant une équipe d'agents dans des tours de communication."""
    def __init__(self, nom_projet: str, objectif: str, agents, n_rounds: int = 5, verbose: bool = False):
        """
        Initialise l'équipe et le système de communication.
        Paramètres:
        - nom_projet : Nom du projet de l'équipe (utilisé pour le contexte, logs, etc.)
        - objectif   : Objectif assigné à l'équipe (description de la tâche à accomplir).
        - agents     : Liste (ou dictionnaire) des agents participants.
        - n_rounds   : Nombre de tours d'interaction prévus.
        - verbose    : Si True, active le mode verbeux (affichage de tous les messages de dialogue).
        """
        self.nom_projet = nom_projet
        self.objectif = objectif
        # Stocker les agents dans une liste ordonnée et un dictionnaire pour référence par nom.
        if isinstance(agents, dict):
            self.agents = list(agents.values())
            self.agents_dict = agents
        else:
            self.agents = list(agents)
            self.agents_dict = {getattr(ag, "name", getattr(ag, "nom", str(i))): ag 
                                for i, ag in enumerate(self.agents)}
        # Créer le module de communication asynchrone pour l'équipe.
        # Cela initialise les files de messages de chaque agent et leur attribue self.communication.
        self.communication = Communication(self.agents, verbose=verbose)
        self.n_rounds = n_rounds
        self.verbose = verbose

    def run(self):
        """Exécute la séquence de tours d'interaction entre les agents."""
        for tour in range(1, self.n_rounds + 1):
            if self.verbose:
                print(f"\n--- Tour {tour} ---")
            # Pour chaque agent, déclencher son traitement des messages reçus et son action éventuelle.
            for agent in self.agents:
                # Chaque agent doit implémenter une méthode process_messages() pour définir son comportement à chaque tour.
                if hasattr(agent, "process_messages"):
                    agent.process_messages()
                else:
                    raise AttributeError(f"L'agent {agent} n'a pas de méthode process_messages() pour traiter son tour.")
        if self.verbose:
            print(f"\n*** Fin des {self.n_rounds} tours d'interaction ***")

    def cloturer(self):
        """
        Termine l'interaction de l'équipe.
        Cette méthode peut être étendue pour réaliser des opérations de finalisation 
        (ex: affichage de résultats, sauvegarde de l'historique, etc.).
        """
        print("Interaction terminée.")
