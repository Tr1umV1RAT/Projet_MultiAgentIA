from teams.base_team import BaseTeam

from agents.agent_project_manager import AgentProjectManager
from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer
from agents.agent_designer import AgentDesigner
from agents.agent_narrateur import AgentNarrateur
from agents.agent_synthetiseur import AgentSynthetiseur

from roles.project_manager import ProjectManagerRole
from roles.codeur import CodeurRole
from roles.reviewer import ReviewerRole
from roles.designer import DesignerRole
from roles.narrateur import NarrateurRole
from roles.synthetiseur import SynthetiseurRole

class CodeTeam(BaseTeam):
    def __init__(self, n_rounds=5, verbose=True, prompt_initial=None, distribuer_prompt_initial=True):
        agents = {
            "ManagerAI": AgentProjectManager(name="ManagerAI", role=ProjectManagerRole(), verbose=verbose),
            "CodeurAI": AgentCodeur(name="CodeurAI", role=CodeurRole(), verbose=verbose),
            "ReviewerAI": AgentReviewer(name="ReviewerAI", role=ReviewerRole(), verbose=verbose),
            "DesignerAI": AgentDesigner(name="DesignerAI", role=DesignerRole(), verbose=verbose),
            "NarrateurAI": AgentNarrateur(name="NarrateurAI", role=NarrateurRole(), verbose=verbose),
            "SynthetiseurAI": AgentSynthetiseur(name="SynthetiseurAI", role=SynthetiseurRole(), verbose=verbose),
        }

        super().__init__(
            nom_team="CodeTeam",
            agents=agents,
            n_rounds=n_rounds,
            verbose=verbose,
            prompt_initial=prompt_initial,
            distribuer_prompt_initial=distribuer_prompt_initial
        )
