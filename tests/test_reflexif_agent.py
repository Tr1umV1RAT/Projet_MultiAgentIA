# tests/test_reflexif_agent.py

from agents.reflexif_agent import AgentReflexif
from roles.base_role import BaseRole
from skills.communication.messages import Message
from roles.base_role import BaseRole

class DummyRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Strategie",
            objectif="Analyser et répondre à des demandes stratégiques complexes"
        )

    def get_prompt(self):
        return "Tu es un assistant stratégique expert en planification, communication et coordination de projet."


agent = AgentReflexif(name="StrategieAI", role=DummyRole(), verbose=True)
message = Message(origine="User", destinataire="StrategieAI", type_message="task", contenu="Propose une stratégie de test d'intégration.")
response = agent.activate(message)
print(response)