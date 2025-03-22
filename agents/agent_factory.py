from agents.agent_registry import AGENT_REGISTRY

class AgentFactory:
    @staticmethod
    def create(agent_type: str, nom=None, role=None, **kwargs):
        if agent_type not in AGENT_REGISTRY:
            raise ValueError(f"Agent inconnu : {agent_type}")
        agent_class = AGENT_REGISTRY[agent_type]
        return agent_class(nom=nom or agent_type.capitalize(), role=role, **kwargs)
