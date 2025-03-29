import argparse
from teams.base_team import BaseTeam
from agents.agent_project_manager import AgentProjectManager
from agents.agent_design_manager import AgentDesignManager
from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer
from agents.agent_narrative_designer import AgentNarrativeDesigner
from skills.communication.messages import Message

class CodeTeam(BaseTeam):
    def __init__(self, name="CodeTeam", project_path="project_outputs", verbose=False, with_narrative=True):
        super().__init__(name=name, project_path=project_path, verbose=verbose)

        self.agents = {
            "ProjectManager": AgentProjectManager(name="ProjectManager", project_path=project_path, verbose=verbose),
            "DesignManager": AgentDesignManager(name="DesignManager", project_path=project_path, verbose=verbose),
            "Codeur": AgentCodeur(name="Codeur", project_path=project_path, verbose=verbose),
            "Reviewer": AgentReviewer(name="Reviewer", project_path=project_path, verbose=verbose),
        }
        if with_narrative:
            self.agents["NarrativeDesigner"] = AgentNarrativeDesigner(name="NarrativeDesigner", project_path=project_path, verbose=verbose)

    def run_round(self, objectif):
        m1 = self.agents["ProjectManager"].dispatch_to_design(objectif)
        self.send_message(m1)
        m2 = self.route_message(m1)
        self.send_message(m2)
        m3 = self.route_message(m2)
        self.send_message(m3)
        if "NarrativeDesigner" in self.agents:
            m4 = self.route_message(m3)
            self.send_message(m4)
        m5 = self.route_message(m4 if "NarrativeDesigner" in self.agents else m3)
        self.send_message(m5)
        m6 = self.route_message(m5)
        self.send_message(m6)
        m7 = Message(
            origine="Système",
            destinataire="ProjectManager",
            contenu="Merci de produire une synthèse du projet",
            action="synthesis",
            type_message="text"
        )
        self.send_message(m7)
        m8 = self.route_message(m7)
        self.send_message(m8)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une CodeTeam pour un projet de code collaboratif.")
    parser.add_argument("objectif", type=str, help="L'objectif ou prompt initial du projet")
    parser.add_argument("--n_round", type=int, default=3, help="Nombre de rounds à effectuer")
    parser.add_argument("--no-reviewer", action="store_true", help="Désactiver le reviewer")
    parser.add_argument("--no-narrator", action="store_true", help="Ne pas inclure de NarrativeDesigner")
    parser.add_argument("--name", type=str, default="CodeTeam", help="Nom de la team ou du projet")
    parser.add_argument("--verbose", action="store_true", help="Afficher les logs détaillés")
    args = parser.parse_args()

    team = CodeTeam(
        name=args.name,
        verbose=args.verbose,
        with_narrative=not args.no_narrator
    )

    if args.no_reviewer:
        team.agents.pop("Reviewer", None)

    for i in range(args.n_round):
        if args.verbose:
            print(f"\n===== ROUND {i + 1} =====\n")
        team.run_round(args.objectif)
