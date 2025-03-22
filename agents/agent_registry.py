from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer
from agents.agent_manager import AgentManager

AGENT_REGISTRY = {
    "codeur": AgentCodeur,
    "reviewer": AgentReviewer,
    "manager": AgentManager
}
