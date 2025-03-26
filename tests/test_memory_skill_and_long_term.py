import time
from tools.llm_wrapper import LLMWrapper
from skills.memory.memory_skill import MemorySkill
from skills.communication.messages import Message
from agents.base_agent import BaseAgent
from roles.role_debateur import RoleDebateur
def test_memory_skill():
    # 🔧 Configuration du wrapper LLM
    agent = BaseAgent(name="Testeur", role=RoleDebateur)
    llm = LLMWrapper(agent=agent)  # adapte selon ton setup

    # 📂 Initialisation du skill mémoire
    skill = MemorySkill(agent_name="Testeur", llm=llm, verbose=True)
    role=RoleDebateur
    # 📨 Création de messages à stocker
    messages = [
        Message(
            origine="AgentA",
            destinataire="AgentB",
            
            type_message="LLM_RESPONSE",
            contenu=(
                "Je pense que les taxes sur les plus-values sont injustes car elles "
                "pénalisent les entrepreneurs qui prennent des risques pour innover."
            ),
            meta={"memoriser": True, role:"DébateurPro"}
        ),
        
        Message(
            origine="AgentB",
            destinataire="AgentA",
            type_message="LLM_RESPONSE",
            
            contenu=(
                "Au contraire, elles permettent de redistribuer équitablement la richesse "
                "et de financer les services publics essentiels."
            ),
            meta={"memoriser": True, role:"DébateurContra"}
        ),
        
        Message(
            origine="AgentA",
            destinataire="AgentB",
            
            type_message="LLM_RESPONSE",
            contenu="Mais cela décourage les investissements productifs à long terme.",
            meta={"memoriser": True,role:"DébateurPro"}
        ),
    ]

    # 💾 Stockage conditionnel des messages
    for message in messages:
        skill.save_interaction(message)
        time.sleep(1)  # Evite les timestamps strictement identiques

    # 🧠 Génération de la mémoire immédiate via mémoire longue
    context_instruction = "Tu prépares un résumé pour aider un modérateur de débat économique entre deux agents IA."
    memoire_immediate = skill.compose_working_memory(context_instruction)

    # 🖨️ Affichage final
    print("\n====== MÉMOIRE IMMÉDIATE GÉNÉRÉE ======\n")
    print(memoire_immediate)
    print("\n========================================\n")


if __name__ == "__main__":
    test_memory_skill()
