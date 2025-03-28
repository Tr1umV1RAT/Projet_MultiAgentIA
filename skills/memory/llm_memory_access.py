from skills.memory.memory_access_strategy import MemoryAccessStrategy

class LLMMemoryAccess(MemoryAccessStrategy):
    def __init__(self, llm_interface, long_term_memory, verbose=False):
        self.llm = llm_interface
        self.ltm = long_term_memory
        self.verbose = verbose

    def retrieve(self, current_message, short_term_context=""):
        # Méthode existante (on ne l'utilise plus directement pour la réponse)
        relevant_messages = self.ltm.retrieve(current_message.contenu, max_results=10)
        
        if not relevant_messages:
            return ""
        
        context_summary = "\n".join(
            f"- {msg.origine} a dit : '{msg.contenu}'" for msg in relevant_messages
        )
        
        # Optionnellement, on pouvait formuler un prompt complet ici, mais nous voulons juste un résumé.
        return context_summary.strip()
    
    def get_summary(self, current_message, short_term_context=""):
        # Retourne simplement un résumé des messages pertinents dans la LTM
        relevant_messages = self.ltm.retrieve(current_message.contenu, max_results=10)
        if not relevant_messages:
            return ""
        summary = "\n".join(f"{msg.origine}: {msg.contenu}" for msg in relevant_messages)
        #if self.verbose:
            #print(f"[LLMMemoryAccess] Summary extrait:\n{summary}\n")
        return summary.strip()
