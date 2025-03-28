from skills.communication.messages import Message

class MemoryManager:
    def __init__(self, stm, ltm, wm, importance_threshold=5):
        self.stm = stm
        self.ltm = ltm
        self.wm = wm
        self.importance_threshold = importance_threshold

    def store_message(self, message: Message):
        self.stm.store(message)
        if message.importance >= self.importance_threshold:
            self.ltm.store(message)

    def store_to_ltm(self, message: Message):
        self.ltm.store(message)

    def get_context(self, query, max_results=3):
        return self.wm.retrieve(query, max_results)

    def clear_all(self):
        self.stm.clear()
        self.ltm.clear()
