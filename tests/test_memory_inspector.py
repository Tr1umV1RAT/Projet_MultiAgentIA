import os
import shutil
from agents.base_agent import BaseAgent
from roles.base_role import BaseRole
from skills.communication.messages import Message
from skills.memory.memory_inspector import MemoryInspectorSkill
from tools.llm_wrapper import LLMWrapper

# ---- Rôle minimal ----
class TestRole(BaseRole):
    def __init__(self):
        super().__init__(name="test", objectif="Évaluer la mémoire de l’agent.")
    def get_prompt(self):
        return "Tu es un agent IA test. Sois concis."


# ---- LLM simulé pour test ----
class DummyLLMWrapper:
    def __init__(self, agent=None, verbose=False):
        self.agent = agent
        self.verbose = verbose
    def ask(self, prompt: str):
        if self.verbose:
            print(f"[DummyLLM] PROMPT :\n{prompt}")
        if "mot de passe" in prompt.lower():
            return Message.system("DummyLLM", self.agent.name, "Plusieurs événements techniques importants ont eu lieu. Certains échanges semblent contenir des informations sensibles.")
        return Message.system("DummyLLM", self.agent.name, "Résumé générique.")


def test_memory_inspector_skill():
    base_path = "/mnt/data/agent_memories"
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    # Agent initialisé avec LLM simulé
    role = TestRole()
    agent = BaseAgent(name="Inspecteur", role=role, verbose=True)
    agent.llm = LLMWrapper(agent=agent, verbose=True)
    agent.memoire.llm = agent.llm

    # Ajout du skill d’inspection
    inspector = MemoryInspectorSkill(verbose=True)
    agent.skills.append(inspector)

    # Injection de souvenirs dans la mémoire
    souvenirs = [
        Message(origine="user", destinataire="Inspecteur", contenu="Le serveur plante si on dépasse 10Mo."),
        Message(origine="admin", destinataire="Inspecteur", contenu="L'API a été redéployée."),
        Message(origine="user", destinataire="Inspecteur", contenu="Le mot de passe est SuperSecret42!"),
        Message(origine="system", destinataire="Inspecteur", contenu="Fin du traitement à 23h59.")
    ]
    
    for msg in souvenirs:
        msg.importance = None
        agent.memoire.save_interaction(msg)

    # Requête d’inspection mémoire
    requete = Message(
        origine="humain",
        destinataire="Inspecteur",
        action="inspect_memory",
        meta={
            "resume_intelligent": True,
            "min_importance": 1,
            "afficher_contenu": True
        }
    )

    print("\n🔍 Lancement de l'inspection mémoire intelligente...\n")
    agent.receive_message(requete)
    agent.process_messages()


if __name__ == "__main__":
    test_memory_inspector_skill()
