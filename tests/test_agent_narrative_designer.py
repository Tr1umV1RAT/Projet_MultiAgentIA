from agents.agent_narrative_designer import AgentNarrativeDesigner
from skills.communication.messages import Message

# Initialisation de l’agent
agent = AgentNarrativeDesigner()

# Création du message d'entrée
message_test = Message.create(
    expediteur="UtilisateurTest",
    destinataire=agent.name,
    contenu="rogue like spatial",
    dialogue=True,
    meta={"project": "test_narratif"}
)

# Traitement du message
response = agent.process_message(message_test)

# Affichage du résultat
print("\n🧠 Réponse de l'Agent Narrative Designer :\n")
print(response.contenu)
print("\n📦 Meta associée :")
print(response.meta)