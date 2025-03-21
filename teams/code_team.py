from .base_team import BaseTeam
from agents.base_agent import BaseAgent
from roles.project_manager import ProjectManager
from roles.developpeur import Developpeur
from roles.narrator import Narrateur
from config import Config
import argparse

class CodeTeam(BaseTeam):
    def __init__(self, nom, agents, schema_db, n_round=5, review=True, test=False, narrator=False, overwrite_db=False):
        super().__init__(nom, agents, schema_db, n_round=n_round, overwrite_db=overwrite_db)
        self.review = review
        self.test = test
        self.narrator = narrator

    @classmethod
    def from_cli(cls):
        parser = argparse.ArgumentParser(description="Équipe de codage explicite.")
        parser.add_argument("objectif", type=str, help="Objectif du projet à coder.")
        parser.add_argument("--name", type=str, default=None, help="Nom explicite du projet.")
        parser.add_argument("--n_round", type=int, default=5, help="Nombre de cycles de développement.")
        parser.add_argument("--no-review", action="store_true", help="Désactive la revue de code.")
        parser.add_argument("--test", action="store_true", help="Active explicitement les tests de code.")
        parser.add_argument("--narrator", action="store_true", help="Active explicitement un narrateur pour le contexte du jeu.")
        parser.add_argument("--overwrite_db", action="store_true", help="Écraser la DB existante explicitement.")
        args = parser.parse_args()

        nom_projet = args.name if args.name else "Projet_Code"
        agents = []

        # Agent principal : Project Manager
        pm = BaseAgent("Project_Manager", role=ProjectManager(args.narrator))
        agents.append(pm)

        # Agent développeur :
        dev = BaseAgent("Codeur", role=Codeur())
        agents.append(dev)

        # Optionnel : Reviewer
        if not args.no_review:
            reviewer = BaseAgent("Reviewer", role=Reviewer())
            agents.append(reviewer)

        # Narrateur optionnel
        if args.narrator:
            narrateur = BaseAgent("Narrateur", role=Narrator())
            agents.append(narrateur)

        return cls(
            nom_projet,
            agents=agents,
            schema_db=Config.MEMORY_SCHEMA,
            n_round=args.n_round,
            review=not args.no_review,
            test=args.test,
            narrator=args.narrator,
            overwrite_db=args.overwrite_db
        )
