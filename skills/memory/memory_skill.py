import os
import re
from datetime import datetime
from skills.base_skill import BaseSkill
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from tools.llm_wrapper import LLMWrapper
from skills.memory.memory_access import MemoryAccessProtocol

class MemorySkill(BaseSkill):
    """
    Skill de gestion mémoire complète pour un agent :
    - Mémoire court terme
    - Mémoire long terme (persistante)
    - Mémoire de travail injectée dans les prompts LLM
    """

    def __init__(self, agent_name: str, llm: LLMWrapper, base_path: str = "/mnt/data/agent_memories", verbose: bool = False, importance_minimale: int = 2):
        self.agent_name = agent_name
        self.verbose = verbose
        self.importance_minimale = importance_minimale

        self.memory_path = self._create_unique_memory_directory(base_path)
        if self.verbose:
            print(f"[MemorySkill] Dossier mémoire initialisé : {self.memory_path}")

        self.short_term = ShortTermMemory(agent_name, self.memory_path)
        self.long_term = LongTermMemory(agent_name, self.memory_path)
        self.llm = llm

    def _create_unique_memory_directory(self, base_path: str) -> str:
        os.makedirs(base_path, exist_ok=True)
        while True:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"{self.agent_name}_{timestamp}"
            full_path = os.path.join(base_path, folder_name)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                return full_path

    def update_short_term(self, messages: list):
        """Ajoute les messages récents à la mémoire courte (non persistante)."""
        self.short_term.add_messages(messages)

    def compose_working_memory(self, context_instruction: str = "") -> str:
        """
        Génère un bloc de mémoire de travail en interrogeant la mémoire longue
        à partir du résumé de la mémoire courte.
        """
        short_context = self.short_term.get_context_summary()
        query = f"{context_instruction}\nVoici le contexte actuel :\n{short_context}\n\nQuelles informations passées sont pertinentes ?"

        if self.verbose:
            print(f"[MemorySkill] Interrogation mémoire long terme :\n{query}")

        retrieved = self.query_llm(query)
        return f"{short_context}\n\n⚠️ Mémoire récupérée :\n{retrieved}"

    def query_llm(self, prompt: str) -> str:
        """
        Compatibilité avec différents types de LLMs (Wrapper, Tool, etc.)
        """
        if hasattr(self.llm, "ask"):
            response = self.llm.ask(prompt)
            return getattr(response, "contenu", str(response))
        elif hasattr(self.llm, "query"):
            return self.llm.query(prompt)
        elif callable(self.llm):
            return self.llm(prompt)
        return "[ERREUR: LLM incompatible]"

    def evaluate_importance(self, message) -> int:
        """
        Demande au LLM d’évaluer l’importance du message (1 à 10).
        """
        prompt = f"""Tu es un assistant IA chargé d’évaluer l’importance d’un message dans le cadre de la mission de l’agent.
Voici le message :
---
{message}
---

Attribue une note entre 1 (sans intérêt) et 10 (critique).
Réponds uniquement par un chiffre entier.
"""
        raw = self.query_llm(prompt)
        match = re.search(r"\b([1-9]|10)\b", raw)
        if match:
            return int(match.group(1))
        if self.verbose:
            print(f"[MemorySkill] Échec de l'évaluation d'importance. Réponse brute : {raw}")
        return 1  # fallback

    def should_memorize(self, message) -> bool:
        """
        Détermine si un message doit être mémorisé, via :
        - son importance (explicite ou évaluée)
        - son flag `.memoriser`
        - son meta["force_memoire"]
        """
        if message.meta.get("force_memoire", False):
            return True

        importance = getattr(message, "importance", None)
        if importance is None or importance <= 0:
            importance = self.evaluate_importance(message)
            message.importance = importance  # mise à jour

        return message.memoriser and importance >= self.importance_minimale

    def save_interaction(self, message):
        """
        Enregistre un message en mémoire s’il est jugé pertinent.
        """
        if self.should_memorize(message):
            self.short_term.store(message)
            self.long_term.store(message)
        elif self.verbose:
            print(f"[MemorySkill] Message ignoré (importance: {message.importance}, memoriser: {message.memoriser})")

    def forget_useless(self):
        """
        Supprime les souvenirs les moins récents ou importants (stratégie simplifiée).
        """
        self.long_term.prune()
   
    def expose_memory(self, filtre: dict, requester: str, access_protocol: MemoryAccessProtocol):
        """
        Donne un accès filtré à la mémoire longue pour un autre agent.
        """
        if not access_protocol.is_authorized():
            raise PermissionError("Non autorisé")

        entries = self.long_term.fetch(
            type_message=filtre.get("type"),
            min_importance=filtre.get("min_importance", 2),
            limit=filtre.get("limit", 50)
        )
        access_protocol.log_access("expose_memory", meta=filtre)
        return entries