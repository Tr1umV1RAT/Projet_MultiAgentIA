from skills.base_skill import BaseSkill

class MemoryRetrieverSkill(BaseSkill):
    def __init__(self, memory_access_strategy, verbose=False):
        self.memory_access_strategy = memory_access_strategy
        self.verbose = verbose

    def retrieve_relevant_memory(self, current_message, short_term_context=""):
        return self.memory_access_strategy.retrieve(current_message, short_term_context)
