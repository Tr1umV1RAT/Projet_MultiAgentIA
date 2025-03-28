import argparse
from teams.base_team import BaseTeam
from agents.agent_debateur import AgentDebateur
from agents.agent_moderateur import AgentModerateur
from agents.agent_synthetiseur import AgentSynthetiseur
from skills.communication.messages import Message

class DebateTeam(BaseTeam):
    def __init__(self, sujet, n_round=5, synthese=True, verbose=False, communication=None):
        self.sujet = sujet
        self.n_round = n_round
        self.verbose = verbose
        self.synthese_activee = synthese

        # Instanciation des agents
        pro = AgentDebateur(name="DébateurPro", camp="POUR", verbose=verbose)
        contra = AgentDebateur(name="DébateurContra", camp="CONTRE", verbose=verbose)
        moderateur = AgentModerateur(name="Modérateur", verbose=verbose)
        synth = AgentSynthetiseur(name="Synthétiseur", verbose=verbose)

        agents = {
            "pro": pro,
            "contra": contra,
            "moderateur": moderateur,
            "synth": synth
        }

        super().__init__(agents=agents, verbose=verbose, nom_team="debate team")

        self.communication.envoyer(Message.system("Système", "ALL", f"Sujet du débat : {self.sujet}"))

    def run(self):
        for _ in range(self.n_round):
            print(f"\n--- Round {_ + 1} ---")
            self.step()

        if self.synthese_activee:
            print("\n📝 Synthèse finale :\n")
            self.agents_dict["synth"].receive_message(Message.system("Système", "Synthétiseur", f"Fais une synthèse du débat suivant :"))
            self.agents_dict["synth"].process_messages()

        if self.verbose:
            self.communication.afficher_messages_visibles()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Débat entre agents IA")
    parser.add_argument("sujet", type=str, help="Sujet du débat")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds")
    parser.add_argument("--synthese", action="store_true", help="Activer la synthèse finale")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    args = parser.parse_args()

    team = DebateTeam(sujet=args.sujet, n_round=args.n_round, synthese=args.synthese, verbose=args.verbose)
    team.run()
