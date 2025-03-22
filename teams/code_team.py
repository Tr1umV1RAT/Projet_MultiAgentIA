import argparse
import os
import sys
import json
from agents.base_agent import BaseAgent
from teams.base_team import BaseTeam
from roles.project_manager import ProjectManagerRole
from roles.codeur import CodeurRole
from roles.reviewer import ReviewerRole
from roles.designer import DesignerRole
from roles.narrator import NarratorRole
from skills.communication import CommunicationSkill
from skills.db_management import DBManagementSkill
from skills.memory.long_term import LongTermMemorySkill
from utils.project_io import create_project_dir, save_project_state, load_project_state


class CodeTeam(BaseTeam):
    def __init__(self, name, agents, project_path, n_round=5):
        super().__init__(name=name, agents=agents, n_round=n_round)
        self.project_path = project_path

    def save_state(self):
        save_project_state(self, self.project_path)

    def load_state(self):
        data = load_project_state(self.project_path)
        # Implémenter la restauration des agents, messages, etc...
        # Placeholder pour l'instant
        pass


def parse_args():
    parser = argparse.ArgumentParser(description="Lance une CodeTeam pour réaliser un projet de code collaboratif.")
    parser.add_argument("prompt", type=str, help="Description du projet")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds")
    parser.add_argument("--no-review", action="store_true", help="Désactive le reviewer")
    parser.add_argument("--test", action="store_true", help="Active les tests automatiques")
    parser.add_argument("--narrator", action="store_true", help="Ajoute un narrateur")
    parser.add_argument("--name", type=str, help="Nom du projet (facultatif)")
    parser.add_argument("--load", type=str, help="Chemin vers un projet existant à charger")
    return parser.parse_args()


def build_agents(args):
    agents = []

    pm = BaseAgent(name="Manager", role=ProjectManagerRole(), skills=[CommunicationSkill(), DBManagementSkill(), LongTermMemorySkill()])
    agents.append(pm)

    designer = BaseAgent(name="Designer", role=DesignerRole(), skills=[CommunicationSkill(), DBManagementSkill(), LongTermMemorySkill()])
    agents.append(designer)

    codeur = BaseAgent(name="Codeur", role=CodeurRole(), skills=[CommunicationSkill(), DBManagementSkill(), LongTermMemorySkill()])
    agents.append(codeur)

    if not args.no_review:
        reviewer = BaseAgent(name="Reviewer", role=ReviewerRole(), skills=[CommunicationSkill(), DBManagementSkill(), LongTermMemorySkill()])
        agents.append(reviewer)

    if args.narrator:
        narrator = BaseAgent(name="Narrateur", role=NarratorRole(), skills=[CommunicationSkill(), DBManagementSkill(), LongTermMemorySkill()])
        agents.append(narrator)

    return agents


def main():
    args = parse_args()

    if args.load:
        project_path = args.load
        code_team = load_project_state(project_path)
        code_team.run()
        return

    name = args.name if args.name else args.prompt.replace(" ", "_")[:30]
    project_path = create_project_dir(name)

    agents = build_agents(args)
    code_team = CodeTeam(name=name, agents=agents, project_path=project_path, n_round=args.n_round)
    code_team.run()
    code_team.save_state()


if __name__ == "__main__":
    main()
