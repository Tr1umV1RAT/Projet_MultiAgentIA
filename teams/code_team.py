import argparse
from agents.base_agent import BaseAgent
from base_team import BaseTeam
from roles.project_manager import ProjectManagerRole
from roles.codeur import CodeurRole
from roles.reviewer import ReviewerRole
from roles.project_designer import ProjectDesignerRole
from roles.narrator import NarratorRole  # à créer si besoin
from tools.project_io import create_project_dir, save_project_state, load_project_state


class CodeTeam(BaseTeam):
    def __init__(self, prompt, name=None, n_round=5, use_reviewer=True, use_test=False, use_narrator=False):
        self.name = name or f"code_project_{prompt[:10].replace(' ', '_')}"
        self.project_path = create_project_dir(self.name)
        self.use_reviewer = use_reviewer
        self.use_test = use_test
        self.use_narrator = use_narrator

        agents = [
            BaseAgent("Project Manager", ProjectManagerRole()),
            BaseAgent("Codeur", CodeurRole()),
            BaseAgent("Project Designer", ProjectDesignerRole())
        ]
        if use_reviewer:
            agents.append(BaseAgent("Reviewer", ReviewerRole()))
        if use_narrator:
            agents.append(BaseAgent("Narrator", NarratorRole()))

        super().__init__(agents=agents, prompt=prompt, n_round=n_round)

    def run(self):
        print(f"[+] Lancement du projet: {self.name} ({self.n_round} tours)")
        for i in range(self.n_round):
            print(f"[Tour {i+1}/{self.n_round}]")
            self.step()
            save_project_state(self, self.project_path)
        print("[+] Projet terminé")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une CodeTeam IA collaborative")
    parser.add_argument("prompt", type=str, help="Objectif initial du projet (ex: 'Créer un jeu')")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de tours d'interaction")
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
            name=args.name,
            n_round=args.n_round,
            use_reviewer=not args.no_review,
            use_test=args.test,
            use_narrator=args.narrator
        )
        team.run()
