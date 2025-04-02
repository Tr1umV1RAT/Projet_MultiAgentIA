# teams/code_team.py

from teams.base_team import BaseTeam
from agents.agent_project_manager import AgentProjectManager
from agents.agent_design_manager import AgentDesignManager
from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer
from agents.agent_narrative_designer import AgentNarrativeDesigner

from roles.team_project_manager_role import RoleTeamProjectManager
from roles.team_design_manager_role import RoleTeamDesignManager
from roles.team_codeur_role import RoleTeamCodeur
from roles.team_reviewer_role import RoleTeamReviewer
from roles.team_narrative_designer_role import RoleTeamNarrativeDesigner

from tools.project_saver import save_project_state, load_project_state
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.memory_manager import MemoryManager

class CodeTeam(BaseTeam):
    def __init__(self, objectif, name="CodeTeam", project_path="project_outputs", n_round=5,
                 include_narrator=False, max_review_cycles=3, enable_tests=False, verbose=False):
        super().__init__(name=name, project_path=project_path, verbose=verbose)

        self.objectif = objectif
        self.n_round = n_round
        self.include_narrator = include_narrator
        self.max_review_cycles = max_review_cycles
        self.enable_tests = enable_tests

        self.agents = {
            "ProjectManager": AgentProjectManager(role=RoleTeamProjectManager(), verbose=verbose),
            "DesignManager": AgentDesignManager(role=RoleTeamDesignManager(), verbose=verbose),
            "Codeur": AgentCodeur(role=RoleTeamCodeur(), verbose=verbose),
            "Reviewer": AgentReviewer(role=RoleTeamReviewer(), verbose=verbose)
        }

        if include_narrator:
            self.agents["NarrativeDesigner"] = AgentNarrativeDesigner(role=RoleTeamNarrativeDesigner(), verbose=verbose)

    @classmethod
    def from_saved_state(cls, path, verbose=False):
        state = load_project_state(path)
        instance = cls(
            objectif=state.get("objectif", "Objectif non spécifié"),
            name=state["team_name"],
            project_path=state["project_path"],
            verbose=verbose
        )

        for name, conf in state["agents"].items():
            ltm = LongTermMemory(path=conf["ltm_path"])
            memory = MemoryManager(ltm=ltm)

            if name == "ProjectManager":
                agent = AgentProjectManager(role=RoleTeamProjectManager(), memory=memory, verbose=verbose)
            elif name == "DesignManager":
                agent = AgentDesignManager(role=RoleTeamDesignManager(), memory=memory, verbose=verbose)
            elif name == "Codeur":
                agent = AgentCodeur(role=RoleTeamCodeur(), memory=memory, verbose=verbose)
            elif name == "Reviewer":
                agent = AgentReviewer(role=RoleTeamReviewer(), memory=memory, verbose=verbose)
            elif name == "NarrativeDesigner":
                agent = AgentNarrativeDesigner(role=RoleTeamNarrativeDesigner(), memory=memory, verbose=verbose)
            else:
                continue

            instance.agents[name] = agent

        instance.history = state["history"]
        return instance

    def run(self):
        for round_id in range(1, self.n_round + 1):
            print(f"\n=== Round {round_id}/{self.n_round} ===")
            self.run_round(self.objectif, max_review_rounds=self.max_review_cycles)
            save_project_state(self, output_dir=f"{self.project_path}/state")
            print("💾 État du projet sauvegardé.\n")

    def run_round(self, objectif, max_review_rounds=3):
        # 1. PM transmet au DesignManager
        msg_plan = self.agents["ProjectManager"].transmit_to_design_manager(objectif)
        self.send_message(msg_plan)

        # 2. DesignManager produit le plan d'architecture
        plan_msg = self.route_message(msg_plan)
        self.send_message(plan_msg)

        # 3. Codeur implémente la première version selon le plan
        code_msg = self.agents["Codeur"].receive_message(
            plan_msg.copy_for("Codeur", metadata={"action": "coder", "first_call": True})
        )
        self.send_message(code_msg)

        # 4. NarrativeDesigner (optionnel) commente le code
        if self.include_narrator and "NarrativeDesigner" in self.agents:
            narration_msg = self.agents["NarrativeDesigner"].receive_message(
                code_msg.copy_for("NarrativeDesigner", metadata={"type": "code"})
            )
            self.send_message(narration_msg)

            # 5. Codeur réagit au feedback narratif
            code_msg = self.agents["Codeur"].receive_message(
                narration_msg.copy_for("Codeur", metadata={"action": "coder", "first_call": False})
            )
            self.send_message(code_msg)

        # 6. Boucle Codeur ↔ Reviewer jusqu'à validation ou limite atteinte
        validated = False
        review_round = 0

        while not validated and review_round < max_review_rounds:
            review_msg = self.agents["Reviewer"].receive_message(
                code_msg.copy_for("Reviewer", metadata={"action": "review", "type": "code", "test": self.enable_tests})
            )
            self.send_message(review_msg)
            review_round += 1

            if review_msg.metadata.get("status") == "validated":
                validated = True
                break

            # Codeur corrige le code en tenant compte du review + plan initial + narration
            code_msg = self.agents["Codeur"].receive_message(
                review_msg.copy_for("Codeur", metadata={"action": "coder", "first_call": False})
            )
            self.send_message(code_msg)

        # 7. PM synthétise le round
        synth_msg = self.agents["ProjectManager"].synthesize_round()
        self.send_message(synth_msg)
