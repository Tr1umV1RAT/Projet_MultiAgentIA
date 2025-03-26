from skills.communication.messages import Message
from skills.communication.communication import Communication

class BaseTeam:
    """
    Classe de base orchestrant une équipe d'agents pour une discussion interactive.
    La team est responsable d'injecter une stratégie de routage commune via une callback,
    centralisant ainsi la communication entre agents.
    """
    def __init__(self, nom_team: str, agents, n_rounds: int = 5, verbose: bool = False,
                 prompt_initial: str = None, distribuer_prompt_initial: bool = True):
        self.nom_team = nom_team
        self.prompt_initial = prompt_initial
        self.distribuer_prompt_initial = distribuer_prompt_initial
        self.n_rounds = n_rounds
        self.verbose = verbose

        if isinstance(agents, dict):
            self.agents = list(agents.values())
            self.agents_dict = agents
        else:
            self.agents = list(agents)
            self.agents_dict = {getattr(ag, "name", getattr(ag, "nom", str(i))): ag 
                                for i, ag in enumerate(self.agents)}
        
        # Créer une instance commune de Communication pour la team.
        self.communication = Communication(verbose=self.verbose)
        
        # Injecter cette instance commune dans chaque agent et assigner la callback de routage.
        for agent in self.agents:
            agent.communication = self.communication
            agent.communication.set_route_callback(self._route_message)
    
    def _route_message(self, message: Message):
        """
        Callback de routage qui distribue le message aux agents selon le champ 'destinataire'.
        """
        dest = message.destinataire
        if dest is None or (isinstance(dest, str) and dest.lower() in {"all", "tous"}):
            destinataires = list(self.agents_dict.keys())
        elif isinstance(dest, (list, tuple, set)):
            destinataires = []
            for d in dest:
                if isinstance(d, str) and d in self.agents_dict:
                    destinataires.append(d)
                else:
                    nom = getattr(d, "name", None) or getattr(d, "nom", None)
                    if nom and nom in self.agents_dict:
                        destinataires.append(nom)
        else:
            if isinstance(dest, str) and dest in self.agents_dict:
                destinataires = [dest]
            else:
                nom = getattr(dest, "name", None) or getattr(dest, "nom", None)
                destinataires = [nom] if (nom and nom in self.agents_dict) else []
        for name in destinataires:
            self.agents_dict[name].messages.append(message)
        if message.dialogue or message.affichage_force:
            for name, agent in self.agents_dict.items():
                if name in destinataires or name == message.origine:
                    continue
                agent.messages.append(message)

    def envoyer_consigne_team(self):
        """
        Envoie le prompt initial à tous les agents si défini et si l'envoi est activé.
        """
        if self.prompt_initial is not None and self.distribuer_prompt_initial:
            consigne = Message(
                origine="Système",
                destinataire="ALL",
                type_message="system",
                contenu=self.prompt_initial,
                dialogue=True,
                memoriser=False
            )
            for agent in self.agents:
                agent.messages.append(consigne)
        else:
            if self.verbose:
                print("Aucune consigne initiale n'a été envoyée.")

    def run(self):
        self.envoyer_consigne_team()
        if self.verbose:
            if self.prompt_initial is not None and self.distribuer_prompt_initial:
                print(f"Discussion démarrée pour l'équipe '{self.nom_team}' avec le prompt : {self.prompt_initial}")
            else:
                print(f"Discussion démarrée pour l'équipe '{self.nom_team}' sans consigne initiale.")
        for tour in range(1, self.n_rounds + 1):
            if self.verbose:
                print(f"\n--- Tour {tour} ---")
            for agent in self.agents:
                if hasattr(agent, "process_messages"):
                    agent.process_messages()
                else:
                    print(f"L'agent {agent} n'a pas de méthode process_messages() pour traiter son tour.")
        if self.verbose:
            print(f"\n*** Fin des {self.n_rounds} tours d'interaction ***")
    
    def cloturer(self):
        print("\nHistorique complet de la discussion :")
        self.communication.afficher_messages_visibles()
        print("Discussion terminée.")


    def step(self):
        for agent in self.agents:
            if hasattr(agent, "process_messages"):
                agent.process_messages()