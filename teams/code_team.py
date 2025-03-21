import os
from teams.base_team import BaseTeam
from agents.base_agent import BaseAgent
from roles.project_manager import ProjectManager
from roles.codeur_basique import CodeurBasique
from roles.reviewer import Reviewer
from config import Config

class CodeTeam(BaseTeam):
    def __init__(self, nom_projet, objectif, n_rounds=5, use_reviewer=True, overwrite_db=False):
        self.nom_projet = nom_projet
        self.objectif = objectif
        self.n_rounds = n_rounds
        self.use_reviewer = use_reviewer

        dossier = f"teams/{nom_projet}"
        os.makedirs(dossier, exist_ok=True)

        super().__init__(
            nom=nom_projet,
            agents=[],
            schema_db=Config.MEMORY_TABLE_SCHEMA,
            overwrite_db=overwrite_db
        )

        # Création des agents avec rôles explicites
        pm = BaseAgent("ChefProjet", role=ProjectManager())
        dev = BaseAgent("Codeur", role=CodeurBasique())
        self.agents.extend([pm, dev])

        if use_reviewer:
            rev = BaseAgent("Relecteur", role=Reviewer())
            self.agents.append(rev)

        for agent in self.agents:
            agent.memoire_persistante = self.db_skill

    def run(self):
        print(f"🚀 Lancement de la CodeTeam pour : {self.objectif}")
        for round in range(1, self.n_rounds + 1):
            print(f"\n🔁 Round {round}/{self.n_rounds}")
            self.envoyer_consigne_team(self.objectif)
