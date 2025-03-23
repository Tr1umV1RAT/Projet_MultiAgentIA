import argparse
from agents.agent_project_manager import AgentProjectManager
from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer
from agents.agent_project_designer import AgentProjectDesigner
from agents.agent_narrative_designer import AgentNarrativeDesigner

from base_team import BaseTeam
from skills.communication.messages import Message
from tools.project_io import create_project_dir, save_project_state, load_project_state


class CodeTeam(BaseTeam):
    def __init__(self, prompt, name=None, n_rounds=5, verbose=False, verbosity=0, use_reviewer=True, use_test=False, use_narrator=False):
        # Utilise le nom du projet ou génère-le à partir du prompt
        self.nom_team = name or f"code_project_{prompt[:20].replace(' ', '_')}"
        self.project_path = create_project_dir(self.nom_team)
        self.use_reviewer = use_reviewer
        self.use_test = use_test
        self.use_narrator = use_narrator
        self.verbosity = verbosity  # 0 = silencieux, 1 = verbose, 2 = très verbose

        # Instanciation des agents spécialisés
        agents = [
                    AgentProjectManager(verbose=verbosity_level),
                    AgentProjectDesigner(verbose=verbosity_level),
                    AgentCodeur(project_path=self.project_path, verbose=verbosity_level)
        ]              
        if use_narrator:
                   agents.append(AgentNarrativeDesigner(verbose=verbosity_level))

        if use_reviewer:
            agents.append(AgentReviewer(verbose=verbosity_level))
    

        # On passe aux paramètres attendus par BaseTeam : nom_team, agents, n_rounds, verbose, prompt_initial
        super().__init__(nom_team=self.nom_team, agents=agents, n_rounds=n_rounds, verbose=verbose, prompt_initial=prompt)
        
        # Lier la communication entre agents via un routeur commun
        for agent in self.agents:
            agent.communication.set_route_callback(self.route_message)
        
        # Initialiser un historique global pour conserver tous les messages échangés
        self.historique = []

    def step(self):
        """
        Effectue un cycle de traitement pour chaque agent, collecte les messages du tour,
        et affiche un résumé détaillé de l'historique global.
        """
        # Chaque agent traite ses messages
        for agent in self.agents:
            if hasattr(agent, "process_messages"):
                agent.process_messages()
            else:
                print(f"[Warning] L'agent {agent.name} ne possède pas de méthode process_messages().")
        
        # Récupérer les messages envoyés durant ce tour via la communication commune
        if hasattr(self, "communication") and self.communication.outbox:
            messages_du_tour = self.communication.outbox.copy()
            # Ajouter ces messages à l'historique global
            self.historique.extend(messages_du_tour)
            
            # Affichage en fonction du niveau de verbosité
            for msg in messages_du_tour:
                if self.verbosity >= 1:
                    print(f"[Dispatch] {msg.expediteur} -> {msg.destinataire}: {msg.contenu}")
                if self.verbosity >= 2:
                    print(f"[Dispatch - Détail] {msg}")
            
            # Vider l'outbox pour le prochain tour
            self.communication.outbox.clear()
        
        # Afficher l'historique global enrichi à la fin du tour
        print("\n===== Historique global des échanges jusqu'à présent =====")
        for idx, msg in enumerate(self.historique, start=1):
            print(f"{idx:03d} | {msg.expediteur} -> {msg.destinataire} : {msg.contenu}")
        print("============================================================\n")

    def run(self):
        print(f"[+] Lancement du projet: {self.nom_team} ({self.n_rounds} tours)")
        # Envoyer la consigne initiale à tous les agents (via BaseTeam.envoyer_consigne_team())
        self.envoyer_consigne_team()
        for tour in range(1, self.n_rounds + 1):
            print(f"\n--- Tour {tour}/{self.n_rounds} ---")
            self.step()
            save_project_state(self, self.project_path)
            if self.verbosity >= 1:
                print(f"[Verbose] Fin du tour {tour}.")
        print("\n*** Fin des tours d'interaction ***")
        # Optionnel : afficher l'historique complet de la discussion
        if self.verbosity >= 1:
            print("\n===== Historique global des échanges =====")
            for msg in self.historique:
                print(f"{msg.expediteur} -> {msg.destinataire}: {msg.contenu}")
    
    def route_message(self, message: Message):
        """
        Méthode de routage qui redistribue un message aux agents selon son champ 'destinataire'.
        """
        if isinstance(message.destinataire, str) and message.destinataire.lower() in {"all", "tous"}:
            for agent in self.agents:
                agent.messages.append(message)
        elif isinstance(message.destinataire, str):
            for agent in self.agents:
                if agent.name == message.destinataire:
                    agent.messages.append(message)
        elif isinstance(message.destinataire, (list, tuple, set)):
            for dest in message.destinataire:
                self.route_message(message.copy_with(destinataire=dest))
        else:
            print(f"[Warning] Destinataire non reconnu dans le message : {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une CodeTeam IA collaborative")
    parser.add_argument("prompt", type=str, help="Objectif initial du projet (ex: 'Créer un jeu')")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de tours d'interaction")
    parser.add_argument("--name", type=str, help="Nom du projet (répertoire)")
    parser.add_argument("--no-review", action="store_true", help="Désactiver le reviewer")
    parser.add_argument("--test", action="store_true", help="Activer le mode test")
    parser.add_argument("--narrator", action="store_true", help="Activer le narrateur")
    parser.add_argument("--load", type=str, help="Charger un projet existant depuis un chemin")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Activer le mode verbeux (-v ou -vv)")
    args = parser.parse_args()

    verbosity_level = args.verbose

    if args.load:
        team = load_project_state(args.load)
        team.verbosity = verbosity_level
        team.run()
    else:
        team = CodeTeam(
            prompt=args.prompt,
            name=args.name,
            n_rounds=args.n_round,
            verbose=(verbosity_level > 0),
            use_reviewer=not args.no_review,
            use_test=args.test,
            use_narrator=args.narrator,
            verbosity=verbosity_level
        )
        team.run()
