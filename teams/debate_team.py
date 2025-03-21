import argparse
import os
from agents.base_agent import BaseAgent
from roles.scientifique import Scientifique
from roles.climato_sceptique import ClimatoSceptique
from .base_team import BaseTeam
from tools.web_search import WebSearchTool

class DebateTeam(BaseTeam):
    def __init__(self, nom, agents, schema_db, n_round=5, web=False, overwrite_db=False):
        super().__init__(nom, agents, schema_db, n_round=n_round, web=web, overwrite_db=overwrite_db)

    @classmethod
    def from_cli(cls, schema_db):
        parser = argparse.ArgumentParser(description="Initialise explicitement une équipe de débat.")
        parser.add_argument("sujet", type=str, help="Sujet explicite du débat.")
        parser.add_argument("-a", "--actors", type=str, default=None, help="Liste des rôles (séparés par virgules).")
        parser.add_argument("--n_round", type=int, default=5, help="Nombre explicite de rounds.")
        parser.add_argument("--web", action="store_true", help="Activation explicite de la recherche web.")
        parser.add_argument("--overwrite_db", action="store_true", help="Écraser la DB existante explicitement.")
        args = parser.parse_args()

        roles_map = {"scientifique": Scientifique, "climato-sceptique": ClimatoSceptique}

        agents = []
        if args.actors:
            noms_acteurs = args.actors.split(",")
        else:
            noms_acteurs = ["scientifique", "climato-sceptique"]

        for nom_role in roles_map.keys():
            if nom_role not in roles_map:
                continue
            role_instance = roles_map[nom_role]()
            if args.web:
                from tools.web_search import WebSearchTool
                if "WebSearchTool" not in [outil.name for outil in role_instance.outils]:
                    role_instance.outils.append(WebSearchTool())
            agent = BaseAgent(nom_role.capitalize(), role_instance)
            agents.append(agent)

        return cls(args.sujet, agents, schema_db=schema_db, n_round=args.n_round, web=args.web, overwrite_db=args.overwrite_db)