from skills.memory.memory_access_strategy import MemoryAccessStrategy

class LLMMemoryAccess(MemoryAccessStrategy):
    def __init__(self, llm_interface, long_term_memory, verbose=False):
        self.llm = llm_interface
        self.ltm = long_term_memory
        self.verbose = verbose

    def retrieve(self, current_message, short_term_context=""):
        relevant_messages = self.ltm.retrieve(current_message.contenu, max_results=5)
        context_summary = "\n".join([msg.contenu for msg in relevant_messages])

        prompt = f"""
        Message actuel : {current_message.contenu}
        Mémoire pertinente : {context_summary}

        Résume ces souvenirs pour une réponse pertinente :
        """

        if self.verbose:
            print(f"[LLMMemoryAccess] Prompt au LLM : {prompt}")

        return self.llm.query(prompt)
