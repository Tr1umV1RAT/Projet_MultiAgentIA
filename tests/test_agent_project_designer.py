# tests/test_agent_project_designer.py

from agents.agent_project_designer import AgentProjectDesigner
from skills.communication.messages import Message

# Crée l'agent avec la mémoire persistante par défaut
agent = AgentProjectDesigner()

# Message de test simulant une consigne initiale de design
message_test = Message.create(
    expediteur="Client",
    destinataire=agent.name,
    contenu="Nous avons besoin d'un système de gestion de projet collaboratif en ligne avec gestion des tâches, des utilisateurs, et des permissions.",
    meta={"instruction": "initial_brief"}
)

# Traitement du message
response = agent.process_message(message_test)

# Affichage des résultats pour validation
print("\n🧠 Réponse de l'Agent ProjectDesigner :\n")
print(response.contenu)
print("\n📦 Meta associée :")
print(response.meta)
