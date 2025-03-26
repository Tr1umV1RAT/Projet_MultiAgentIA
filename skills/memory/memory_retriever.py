from skills.base_skill import BaseSkill
from tools.llm_interface import LLMInterface
from skills.communication.messages import Message

class MemoryRetrieverSkill(BaseSkill):
    """
    Skill responsable de la récupération intelligente de souvenirs depuis la mémoire long-terme,
    à partir du contexte complet de l'agent (rôle, identité, mémoire court-terme).
    Utilisé par MemorySkill (ou les agents) pour composer un prompt enrichi.
    """

    def __init__(self, agent, memory_long_term, llm: LLMInterface, verbose=False):
        self.agent = agent
        self.memory_long_term = memory_long_term
        self.llm = llm
        self.verbose = verbose

    def build_retrieval_prompt(self, current_message: Message, short_term_context: str = "") -> str:
        role_context = self.agent.get_prompt_context()
        agent_identity = f"Nom de l'agent : {self.agent.name}\nObjectif : {getattr(self.agent, 'objectif', 'Non spécifié')}"
        message_content = f"Message actuel :\n{current_message.contenu}"

        prompt = f"""
Tu es une IA de récupération de mémoire pour un agent.

Contexte de rôle :
{role_context}

Identité de l'agent :
{agent_identity}

Mémoire court terme :
{short_term_context}

{message_content}

Quels souvenirs passés de la mémoire long terme peuvent être utiles ici ?
Retourne les extraits pertinents, sans commentaire ni explication.
"""
        return prompt.strip()

    def retrieve_relevant_memory(self, current_message: Message, short_term_context: str = "") -> str:
        prompt = self.build_retrieval_prompt(current_message, short_term_context)

        if self.verbose:
            print(f"[MemoryRetrieverSkill] Prompt de récupération :\n{prompt}\n")

        try:
            if hasattr(self.llm, "ask"):
                response = self.llm.ask(prompt)
                return getattr(response, "contenu", str(response))
            elif hasattr(self.llm, "query"):
                return self.llm.query(prompt)
            elif callable(self.llm):
                return self.llm(prompt)
            else:
                raise ValueError("[MemoryRetrieverSkill] LLM non compatible")
        except Exception as e:
            if self.verbose:
                print(f"[MemoryRetrieverSkill] ⚠️ Erreur : {e}")
            return "[ERREUR: récupération impossible]"
