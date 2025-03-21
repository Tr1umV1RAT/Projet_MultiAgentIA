from teams.base_team import BaseTeam

class DebateTeam(BaseTeam):
    """
    Classe dédiée pour orchestrer un débat contradictoire entre agents.
    
    Cette classe hérite de BaseTeam et peut être utilisée pour lancer
    un débat où deux (ou plusieurs) agents aux rôles opposés échangent leurs arguments.
    """
    def __init__(self, nom_team: str, prompt_initial: str, agents, n_rounds: int = 5, verbose: bool = True,
                 distribuer_prompt_initial: bool = True):
        # Appel du constructeur de BaseTeam avec les valeurs par défaut souhaitées.
        super().__init__(nom_team, agents, n_rounds, verbose, prompt_initial, distribuer_prompt_initial)
        # Vérification simple pour s'assurer que les rôles semblent contradictoires.
        role_names = [agent.role.nom_role for agent in self.agents if hasattr(agent, "role") and agent.role]
        if len(set(role_names)) < 2:
            print("Attention : Un débat contradictoire nécessite des rôles opposés.")

    def run(self):
        """
        Démarre le débat contradictoire.
        
        Ici, nous utilisons la logique standard de BaseTeam, mais on pourrait ajouter une
        alternance stricte ou d'autres règles spécifiques aux débats contradictoires.
        """
        self.envoyer_consigne_team()
        if self.verbose:
            print(f"Débat contradictoire lancé pour l'équipe '{self.nom_team}' avec le prompt : {self.prompt_initial}")
        
        for tour in range(1, self.n_rounds + 1):
            if self.verbose:
                print(f"\n--- Tour {tour} ---")
            for agent in self.agents:
                if hasattr(agent, "process_messages"):
                    agent.process_messages()
                else:
                    print(f"L'agent {agent} ne possède pas de méthode process_messages().")
        if self.verbose:
            print(f"\n*** Fin des {self.n_rounds} tours du débat contradictoire ***")
    
    def cloturer(self):
        """
        Termine le débat contradictoire et affiche l'historique complet des messages échangés.
        """
        print("\nHistorique complet du débat contradictoire :")
        self.communication.afficher_messages_visibles()
        print("Débat terminé.")
