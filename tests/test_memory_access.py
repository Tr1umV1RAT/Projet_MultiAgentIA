import os
import shutil
from agents.base_agent import BaseAgent
from roles.base_role import BaseRole
from skills.memory.memory_access import MemoryAccessProtocol
from skills.communication.messages import Message
from tools.llm_wrapper import LLMWrapper

# --- Rôle de base ---
class TestRole(BaseRole):
    def __init__(self, name):
        super().__init__(name=name, objectif=f"Agent {name}")
    def get_prompt(self):
        return f"Je suis un agent {self.name}"


def test_memory_access_protocol():
    base_path = "/mnt/data/agent_memories"
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    # Agent codeur avec mémoire
    codeur = BaseAgent("Codeur", role=TestRole("Codeur"), verbose=True)
    codeur.llm = LLMWrapper(agent=codeur)
    codeur.memoire.llm = codeur.llm
    codeur.memoire.importance_minimale = 1  # pour test

    # Simuler quelques messages importants
    messages = [
        Message(origine="manager", destinataire="Codeur", contenu="Écris une fonction de tri", importance=6),
        Message(origine="Codeur", destinataire="manager", contenu="Voici la fonction : def tri(l): return sorted(l)", importance=7),
        Message(origine="manager", destinataire="Codeur", contenu="N'oublie pas d'ajouter un test unitaire", importance=5),
    ]
    for msg in messages:
        codeur.memoire.save_interaction(msg)

    # Agent manager (pas de mémoire ici, il lit celle du codeur)
    manager = BaseAgent("Manager", role=TestRole("Manager"), verbose=True)

    # Protocole d'accès
    access = MemoryAccessProtocol(requester="Manager", target_agent_name="Codeur")
    print("\n🕵️ Lecture de la mémoire du Codeur par le Manager...\n")
    souvenirs = access.read(codeur.memoire.long_term, filtre={"min_importance": 5})

    for entry in souvenirs:
        msg = entry["content"]
        if isinstance(msg, Message):
            print(f"🧠 {msg.date:%H:%M:%S} [{msg.origine}] ➜ {msg.destinataire} : {msg.contenu[:100]}")
        else:
            print(f"💤 Non converti : {entry}")

    # Afficher les logs d'accès
    print("\n📜 Journal des accès :\n")
    for log in access.get_logs():
        print(log)


if __name__ == "__main__":
    test_memory_access_protocol()
