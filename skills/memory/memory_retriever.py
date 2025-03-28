from skills.base_skill import BaseSkill

class MemoryRetrieverSkill(BaseSkill):
    def __init__(self, memory_access_strategy, verbose=False):
        self.memory_access_strategy = memory_access_strategy
        self.verbose = verbose

    def retrieve_relevant_memory(self, current_message, short_term_context=""):
        # On conserve la méthode existante au cas où
        return self.memory_access_strategy.retrieve(current_message, short_term_context)
    
    def get_memory_summary(self, current_message, short_term_context=""):
        return self.memory_access_strategy.get_summary(current_message, short_term_context)
