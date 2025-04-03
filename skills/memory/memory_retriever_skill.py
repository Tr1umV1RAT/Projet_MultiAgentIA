# skills/memory/memory_retriever_skill.py

from skills.base_skill import BaseSkill
from skills.communication.prompt_builder import PromptBuilder

class MemoryRetrieverSkill(BaseSkill):
    name = "memory_retriever"

    def __init__(self,memory_access_strategy, agent, verbose=False):
        self.memory_access_strategy = memory_access_strategy
        self.agent = agent
        self.memory = getattr(agent, "memory", None)
        self.verbose = verbose

        # Profil par défaut si aucun profil explicite n'est fourni
        self.default_profile = {
            "include": ["plan", "code", "review", "narration"],
            "limit": 5,
            "phase": "implémentation"
        }

    def build_context(self, message: "Message") -> dict:
        profile = message.metadata.get("context_profile") \
                  or getattr(self.agent, "context_profile", None) \
                  or self.default_profile

        context = {
            "instruction": message.contenu,
            "phase": profile.get("phase", "implémentation"),
            "memory": self._get_memory_summary(profile.get("limit", 5))
        }

        for key in profile.get("include", []):
            context[key] = self._get_last_memory_by_type(key)

        return context

    def _get_last_memory_by_type(self, type_str):
        if not self.memory:
            return None
        try:
            results = self.memory.ltm.retrieve(query={}, max_results=20)
            for msg in reversed(results):
                if msg.metadata.get("type") == type_str:
                    return msg.contenu
        except Exception as e:
            if self.verbose:
                print(f"[Retriever] Erreur lors de la recherche de type '{type_str}': {e}")
        return None

    def _get_memory_summary(self, limit=5):
        if not self.memory:
            return None
        try:
            entries = self.memory.ltm.retrieve(query={}, max_results=limit)
            return "\n\n".join(f"[{m.metadata.get('type','?')}] {m.contenu}" for m in entries if hasattr(m, "contenu"))
        except Exception as e:
            if self.verbose:
                print(f"[Retriever] Erreur lors de la récupération mémoire: {e}")
            return None

    def retrieve_relevant_memory(self, current_message, short_term_context=""):
        # On conserve la méthode existante au cas où
        return self.memory_access_strategy.retrieve(current_message, short_term_context)
    
    def get_memory_summary(self, message):
        if self.verbose:
            print(f"[MemoryRetrieverSkill] Résumé de mémoire demandé pour : {message.contenu}")

        recent = self.memory.retrieve(query={}, max_results=10)
        return "\n\n".join([m.contenu for m in recent])

    def get_latest_validated_code(self):
        results = self.memory.search_documents({"type": "code", "status": "validated"}, limit=1)
        if results:
            return results[0].get("content", None)
        return None