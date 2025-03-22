import os
import uuid
from agents.agent_reviewer import AgentReviewer
from skills.memory.long_term import LongTermMemory
from config import Config
from skills.communication.messages import Message

# Nettoyage préalable (optionnel pour des tests répétables)
DB_PATH = "reviewer_memory_test.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Préparation de la mémoire persistante
memoire = LongTermMemory(db_name=DB_PATH, schema=Config.MEMORY_TABLE_SCHEMA, description="Mémoire test AgentReviewer")

# Initialisation de l'agent
agent = AgentReviewer(nom="ReviewerTest", memoire_persistante=memoire)

# Simuler un message de relecture d’un code Python (mal ou partiellement écrit)
code = '''
# fichier: test_code.py
```python
def somme(a, b):
return a + b
```
'''

message = Message.create(
    expediteur="CodeurTest",
    destinataire="ReviewerTest",
    contenu=code,
    dialogue=False,
    meta={
        "type_message": "code",
        "importance": 2,
        "memoriser": True,
        "action": "review_request",
        "filename": "test_code.py"
    }
)

# Traitement du message
response = agent.process_message(message)

# Affichage et vérifications
print("\n📨 Réponse de l'agent Reviewer :")
print(response.contenu)

print("\n📦 Meta associée :")
print(response.meta)

# Extraction du contenu pour test manuel (ou assertions)
assert "erreur" in response.contenu.lower() or "amélioration" in response.contenu.lower() or "correction" in response.contenu.lower(), \
    "La réponse ne semble pas inclure d'élément de critique explicite."

print("\n✅ Test terminé avec succès.")