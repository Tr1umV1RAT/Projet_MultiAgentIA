from skills.base_skill import BaseSkill

class MemoryRetrieverSkill(BaseSkill):
    def __init__(self, memory_strategy, agent, verbose=False):
        super().__init__()
        self.memory_strategy = memory_strategy
        self.agent_name = agent
        self.verbose = verbose

    def retrieve(self, query, limit=5):
        if self.verbose:
            print(f"[MemoryRetrieverSkill] Récupération des informations pour '{query}' (limite : {limit})")
        results = self.memory_strategy.retrieve(query, limit)  # Correction ici
        return results

    def build_context(self, message, limit=5):
        retrieved_messages = self.retrieve(message.contenu, limit)

        context_memory = "\n".join(
            [f"[{msg.date.strftime('%Y-%m-%d %H:%M')}] {msg.origine}: {msg.contenu}" for msg in retrieved_messages 
             if hasattr(msg, 'contenu') and msg.contenu != message.contenu]
        )

        context = {
            "memory": context_memory if context_memory else "Aucune mémoire pertinente trouvée.",
            "instruction": message.contenu
        }

        if self.verbose:
            print(f"[MemoryRetrieverSkill] Contexte mémoire construit pour le message '{message.contenu}' :\n{context['memory']}")

        return context
