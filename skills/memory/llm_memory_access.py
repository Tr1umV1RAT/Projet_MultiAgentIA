from skills.memory.long_term_memory import LongTermMemory

class LLMMemoryAccess:
    def __init__(self, llm, ltm: LongTermMemory, verbose=False):
        self.llm = llm
        self.ltm = ltm
        self.verbose = verbose

    def retrieve(self, query, limit=5):
        # Correction explicite : utiliser directement query (string), pas current_message.contenu
        relevant_messages = self.ltm.retrieve(query, max_results=10)

        prompt = (
            f"Voici une liste de messages précédents liés à '{query}' :\n\n"
            + "\n".join([msg.contenu for msg in relevant_messages])
            + f"\n\nSélectionne les {limit} plus pertinents pour répondre précisément à la requête '{query}' :"
        )

        relevant_selection = self.llm.query(prompt)

        # Logique éventuelle à ajuster selon format réponse du LLM
        selected_messages = [
            msg for msg in relevant_messages if msg.contenu in relevant_selection
        ][:limit]

        if self.verbose:
            print(f"[LLMMemoryAccess] Messages sélectionnés pour '{query}': {selected_messages}")

        return selected_messages
