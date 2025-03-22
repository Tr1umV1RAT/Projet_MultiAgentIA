from agents.agent_codeur import AgentCodeur
from skills.db_management.db_management import DBManagementSkill
from skills.memory.long_term import LongTermMemory
from skills.communication.messages import Message
from config import Config

# Instanciation avec mémoire persistante
memoire = LongTermMemory("codeur_memory.db", Config.MEMORY_TABLE_SCHEMA)
agent = AgentCodeur()

# Création d'un message à traiter
message_test = Message.create(
    expediteur="testeur",
    destinataire=agent.name,
    contenu="Écris une fonction Python qui calcule la moyenne d'une liste de nombres.",
    dialogue=True,
)

# Traitement du message
response = agent.process_message(message_test)

# Affichage de la réponse générée
print(f"\n🧠 Réponse de l'agent :\n{response.contenu}")

# Affichage de ce qui a été stocké en base
db = agent.get_skill(DBManagementSkill)
stored = db.recall_messages(limit=1)
print("\n📦 Message stocké en base :")
for entry in stored:
    print(f"\nAuteur     : {entry[5]}")
    print(f"Type       : {entry[3]}")
    print(f"Fichier    : {entry[6]}")
    print(f"Contenu    :\n{entry[4]}")
