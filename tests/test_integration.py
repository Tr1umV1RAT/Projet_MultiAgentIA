# test_integration.py

import os
from datetime import datetime
from tools.llm_adapter import LLMAdapterTool
from skills.reasoning import Reasoning 


# --- Dummy implementations pour le test ---

class DummyRole:
    def generer_prompt(self):
        return "Contexte de DummyRole"
    # Pas d'outils supplémentaires pour ce test
    outils = []

# Un agent simple héritant de BaseAgent et doté d'une file de messages
from agents.base_agent import BaseAgent
class DummyAgent(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(name, role, verbose=verbose)
        self.messages = []  # File de messages reçus

# --- Import des modules du projet ---
from skills.memory.long_term import LongTermMemory
from skills.db_management.db_management import DBManagementSkill
from skills.communication.communication import Communication
from skills.communication.messages import Message

def main():
    # Pour un test propre, on supprime les fichiers de DB existants
    if os.path.exists("long_term_memory.db"):
        os.remove("long_term_memory.db")
    if os.path.exists("agent_messages.db"):
        os.remove("agent_messages.db")

    # Instanciation du rôle et de l'adaptateur LLM
    role = DummyRole()
    llm_adapter = LLMAdapterTool()

    # Création d'un agent dummy
    agent = DummyAgent("Agent1", role, verbose=True)

    # Création d'une instance de Communication avec cet agent
    comm = Communication(agents=[agent], verbose=True)

    # Instanciation de LongTermMemory et DBManagementSkill
    long_term_memory = LongTermMemory(db_name="long_term_memory.db")
    db_management = DBManagementSkill(db_name="agent_messages.db", verbose=True)

    # Création d'une instance de Reasoning avec l'adaptateur LLM
    reasoning = Reasoning(agent, llm_adapter, verbose=True)

    # Construction d'un message de test sous forme de dictionnaire (qui sera converti en Message)
    test_message_data = {
        "origine": agent.name,
        "destinataire": "ALL",    # Broadcast
        "type_message": "text",
        "contenu": "Ceci est un test de message pour l'adaptateur LLM",
        "importance": 1,
        "memoriser": True,
        "dialogue": True,
        "action": "",
        "affichage_force": False,
        "version_finale": False,
        "meta": {}
    }
    message = Message.create(test_message_data)

    # Envoi du message via Communication
    comm.envoyer(message)

    print("\n--- Messages reçus par l'agent ---")
    for m in agent.messages:
        print(m)

    # Traitement du message par Reasoning via l'adaptateur LLM (Ollama)
    response = reasoning.execute(message)
    print("\n--- Réponse du Reasoning ---")
    print(response)

    # Sauvegarde du message dans LongTermMemory et DBManagementSkill
    long_term_memory.save(message)
    recalled = long_term_memory.recall(limit=5)
    print("\n--- Messages dans LongTermMemory ---")
    for r in recalled:
        print(r)

    db_management.save_message(message)
    messages_db = db_management.get_messages(limit=5)
    print("\n--- Messages dans DBManagementSkill ---")
    for m_db in messages_db:
        print(m_db)

    # Fermeture des connexions aux bases de données
    long_term_memory.close()
    db_management.close()

if __name__ == "__main__":
    main()

