
class WorkingMemory:
    def __init__(self, llm, long_term_memory):
        self.llm = llm
        self.long_term_memory = long_term_memory

    def retrieve(self, query, max_results=5):
        # On délègue simplement à la LTM ici.
        return self.long_term_memory.retrieve(query, max_results)
