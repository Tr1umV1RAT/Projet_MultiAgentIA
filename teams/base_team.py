import os
from skills.db_management.db_management import DBManagementSkill
from skills.communication.messages import Message
from agents.base_agent import BaseAgent
import argparse

class BaseTeam:
    def __init__(self, nom, agents, schema_db, n_round=5, web=False, overwrite_db=False):
        self.nom = nom
        self.agents = agents
        self.n_round = n_round
        self.web = web
        
        # Création automatique du dossier du projet
        self.dossier = os.path.join("teams", self.nom)
        os.makedirs(self.dossier, exist_ok=True)

        # Base de données mémoire projet avec gestion explicite
        self.db_skill = DBManagementSkill(
            f"{self.dossier}/{nom}_memory.db",
            schema=schema_db,
            overwrite=overwrite_db,
            adapt_name_if_exists=True
        )

        # Affectation explicite de la mémoire persistante commune à tous les agents
        for agent in self.agents:
            agent.memoire_persistante = self.db_skill

        self.n_round = n_round
        self.web = web

    @classmethod
    def from_cli(cls, schema_db):
        parser = argparse.ArgumentParser()
        parser.add_argument("sujet", help="Sujet explicite du débat ou du projet.")
        parser.add_argument("-a", "--actors", type=str, default=None, help="Acteurs impliqués séparés par des virgules.")
        parser.add_argument("--n_round", type=int, default=5, help="Nombre explicite de rounds.")
        parser.add_argument("--web", action="store_true", help="Activation explicite de la recherche web.")
        parser.add_argument("--overwrite_db", action='store_true', help="Écrase explicitement la base existante.")

        args = parser.parse_args()

        self.nom = args.sujet
        self.n_round = args.n_round
        self.web = args.web
        self.projet_dir = os.path.join("teams", self.nom)
        os.makedirs(self.projet_dir, exist_ok=True)

        agents = []

        roles_map = {"scientifique": Scientifique, "climato-sceptique": ClimatoSceptique}

        if args.actors is None:
            agents = [
                BaseAgent("Scientifique", roles_map["scientifique"]()),
                BaseAgent("Sceptique", roles_map["climato-sceptique"]())
            ]
        else:
            for role_name in args.actors.split(","):
                RoleClass = roles_map.get(role_name.strip().lower(), None)
                if RoleClass:
                    role_instance = RoleClass()
                    if self.web:
                        from tools.web_search_tool import WebSearchTool
                        if "WebSearchTool" not in [outil.nom for outil in role_instance.outils]:
                            role_instance.outils.append(WebSearchTool())
                    agent = BaseAgent(role_name.capitalize(), role_instance)
                    agents.append(agent)

        self.agents = agents

        self.db_skill = DBManagementSkill(
            f"{self.projet_dir}/{self.nom}_memory.db",
            schema=schema_db,
            adapt_name_if_exists=True,
            overwrite=False
        )

        # Mémoire persistante pour chaque agent
        for agent in self.agents:
            agent.memoire_persistante = self.db_skill

        print(f"✅ Team '{self.nom}' initialisée avec {len(self.agents)} agents.")

    def envoyer_consigne_team(self, consigne, destinataire="tous"):
        """Envoi explicite de consigne à toute la team ou à certains agents"""
        message = Message("System", destinataire, consigne, memoriser=True)
        for round in range(self.n_round):
            print(f"\n🔄 Round {round+1}/{self.n_round} :")
            for agent in self.agents:
                agent.communication.envoyer(message)
                agent.communication.recevoir(agent)

    def cloturer(self):
        """Fermeture explicite de la DB"""
        self.db_skill.close()
