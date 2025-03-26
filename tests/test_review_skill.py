from agents.agent_reviewer import AgentReviewer
from roles.reviewer import ReviewerRole
from skills.communication.messages import Message

if __name__ == "__main__":
    # Instanciation de l'agent reviewer
    reviewer = AgentReviewer(name="ReviewerAI", role=ReviewerRole(), verbose=True)

    # Simulation d’un message contenant du code Python
    message = Message(
        origine="CodeurAI",
        destinataire="ReviewerAI",
        type_message="code",
        contenu="# fichier: main.py\n```python\ndef add(a, b):\n    return a+b\n```",
        meta={"filename": "main.py"},
        conversation_id="test-001"
    )

    # Envoi du message au reviewer
    reviewer.receive_message(message)

    # Traitement
    reviewer.process_messages()
