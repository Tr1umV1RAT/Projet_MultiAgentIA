from agents.agent_project_manager import AgentProjectManager
from skills.communication.messages import Message

# Simulation d’un message indiquant des étapes de projet
message = Message.create(
    expediteur="AgentCodeur",
    destinataire="AgentProjectManager",
    contenu="J’ai terminé le module d’authentification et le routeur API. Le reviewer n’a pas encore donné son avis.",
    dialogue=True
)

manager = AgentProjectManager()
reponse = manager.process_message(message)

print("\n🧠 Réponse du Project Manager :\n")
print(reponse.contenu)
