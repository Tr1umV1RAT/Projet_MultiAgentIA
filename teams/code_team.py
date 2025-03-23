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
    def __init__(self, prompt, name=None, n_rounds=5, use_reviewer=True, use_test=False, use_narrator=False):
        self.name = name or f"code_project_{prompt[:20].replace(' ', '_')}"
        self.project_path = create_project_dir(self.name)
        self.use_reviewer = use_reviewer
        self.use_test = use_test
        self.use_narrator = use_narrator

        agents = [
            AgentProjectManager(),
            AgentCodeur(),
            AgentProjectDesigner()
        ]
        if use_reviewer:
            agents.append(AgentReviewer())
        if use_narrator:
            agents.append(AgentNarrativeDesigner())

        super().__init__(
                nom_team=name,
                agents=agents,
                n_rounds=n_rounds,
                prompt_initial=prompt,
                distribuer_prompt_initial=True
            )

        # Lier la communication entre agents via self.route_message
        for agent in self.agents:
            agent.communication.set_route_callback(self.route_message)

        # Injecter un message initial
        self.message_initial = Message.create(
            expediteur="System",
            destinataire="ProjectDesigner",
            contenu=prompt,
            dialogue=True,
            meta={"type_message": "initial_prompt"}
        )

    def run(self):
        print(f"[+] Lancement du projet: {self.name} ({self.n_rounds} tours)")

        # Envoyer prompt initial au ProjectDesigner
        self.dispatch_message(self.message_initial)

        for i in range(self.n_rounds):
            print(f"[Tour {i+1}/{self.n_rounds}]")
            self.step()
            save_project_state(self, self.project_path)

        print("[+] Projet terminé")

    def dispatch_message(self, message):
        if isinstance(message.destinataire, str):
            dest = next((a for a in self.agents if a.name == message.destinataire), None)
            if dest:
                dest.messages.append(message)
        elif isinstance(message.destinataire, list):
            for dest_name in message.destinataire:
                self.dispatch_message(message.copy_with(destinataire=dest_name))
        elif message.destinataire in {"ALL", "all", "tous", "Tous"}:
            for agent in self.agents:
                agent.messages.append(message)

    def route_message(self, message: Message):
        self.dispatch_message(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une CodeTeam IA collaborative")
    parser.add_argument("prompt", type=str, help="Objectif initial du projet (ex: 'Créer un jeu')")
    parser.add_argument("--n_rounds", type=int, default=5, help="Nombre de tours d'interaction")
    parser.add_argument("--name", type=str, help="Nom du projet (répertoire)")
    parser.add_argument("--no-review", action="store_true", help="Désactiver le reviewer")
    parser.add_argument("--test", action="store_true", help="Activer le mode test")
    parser.add_argument("--narrator", action="store_true", help="Activer le narrateur")
    parser.add_argument("--load", type=str, help="Charger un projet existant depuis un chemin")

    args = parser.parse_args()

    if args.load:
        team = load_project_state(args.load)
        team.run()
    else:
        team = CodeTeam(
        prompt=args.prompt,
        n_rounds=args.n_rounds,
        name=args.name,
        use_reviewer=not args.no_review,
        use_narrator=args.narrator,
        use_test=args.test
        )
        team.run()