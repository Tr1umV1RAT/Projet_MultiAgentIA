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
        self.round_index = 0

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

        # Lancement initial du sujet
        self.communication.envoyer(
            Message.system("Système", "ALL", f"Sujet du débat : {self.sujet}", dialogue=True)
        )

    def run(self):
        for _ in range(self.n_round):
            self.round_index += 1
            print(f"\n--- Round {self.round_index} ---")
            self.step()

        if self.synthese_activee:
            print("\n📝 Synthèse finale :\n")
            self.agents_dict["synth"].receive_message(
                Message.system("Système", "Synthétiseur", f"Fais une synthèse du débat suivant :", dialogue=True)
            )
            self.agents_dict["synth"].process_messages()

        if self.verbose:
            self.communication.afficher_messages_visibles()

    def step(self):
        # Alternance : pro commence sur les rounds impairs, contra sur pairs
        premier = "pro" if self.round_index % 2 == 1 else "contra"
        second = "contra" if premier == "pro" else "pro"

        # Message du modérateur : distribution de la parole
        self.agents_dict["moderateur"].receive_message(
            Message.system("Système", "Modérateur", f"Round {self.round_index} : à {premier} de commencer.", dialogue=True)
        )

        # Le modérateur parle
        self.agents_dict["moderateur"].process_messages()

        # Le premier agent débat
        self.agents_dict[premier].receive_message(
            Message.system("Modérateur", self.agents_dict[premier].name, f"À vous de commencer le round {self.round_index}.", dialogue=True)
        )
        self.agents_dict[premier].process_messages()

        # Puis le second répond
        self.agents_dict[second].receive_message(
            Message.system("Modérateur", self.agents_dict[second].name, f"À vous de répondre au round {self.round_index}.", dialogue=True)
        )
        self.agents_dict[second].process_messages()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Débat entre agents IA")
    parser.add_argument("sujet", type=str, help="Sujet du débat")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds")
    parser.add_argument("--synthese", action="store_true", help="Activer la synthèse finale")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    args = parser.parse_args()

    team = DebateTeam(sujet=args.sujet, n_round=args.n_round, synthese=args.synthese, verbose=args.verbose)
    team.run()
