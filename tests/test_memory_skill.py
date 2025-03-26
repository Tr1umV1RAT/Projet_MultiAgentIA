import os
import shutil
from agents.base_agent import BaseAgent
from roles.base_role import BaseRole
from skills.communication.messages import Message
from tools.llm_wrapper import LLMWrapper
# Un rôle minimaliste pour le test
class TestRole(BaseRole):
    def __init__(self):
        super().__init__(name="test", objectif="Répondre de façon simple.")
    def get_prompt(self):
        return "Tu es un agent test. Sois concis."

# Un LLM factice si tu veux éviter un vrai appel
class DummyLLMWrapper:
    def __init__(self, agent=None, verbose=False):
        self.agent = agent
        self.verbose = verbose
    def generate(self, prompt: str):
        if self.verbose:
            print(f"[DummyLLM] Prompt reçu :\n{prompt}")
        return "Réponse simulée."

def test_agent_with_memory():
    # Nettoyage avant/après
    base_path = "/mnt/data/agent_memories"
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    # Création de l'agent avec un rôle test et LLM mocké
    role = TestRole()
    agent = BaseAgent(name="AgentTest", role=role, verbose=True)
    agent.llm = LLMWrapper(agent=agent, verbose=True)
    agent.memoire.llm = agent.llm  # réinjection dans MemorySkill

    # Création d'un message fictif
    message = Message(
        origine="systeme",
        destinataire="AgentTest",
        type_message="user",
        contenu="Dis bonjour.",
        dialogue=True,
        memoriser=True
    )

    # Envoie le message à l'agent
    agent.receive_message(message)

    # Exécution du traitement
    agent.process_messages()

    # Vérifications
    print("\n✅ Mémoire immédiate :")
    print(agent.memoire.compose_working_memory())

    print("\n✅ Historique mémoire court terme :")
    print(agent.memoire.short_term.get_context_summary())

    print("\n✅ Base mémoire long terme :")
    db_path = os.path.join(agent.memoire.memory_path, "long_term_memory.db")
    print(f"Base créée : {os.path.exists(db_path)}")

if __name__ == "__main__":
    test_agent_with_memory()
