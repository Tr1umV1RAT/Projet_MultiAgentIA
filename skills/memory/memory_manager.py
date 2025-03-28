from skills.communication.messages import Message

class MemoryManager:
    def __init__(self, stm, ltm, wm, importance_threshold=1):  # Seuil passé à 1
        self.stm = stm
        self.ltm = ltm
        self.wm = wm
        self.importance_threshold = importance_threshold

    def store_message(self, message: Message):
        self.stm.store(message)
        # On stocke dans la LTM si l'importance du message est >= seuil
        if message.importance >= self.importance_threshold:
            self.ltm.store(message)

    def store_to_ltm(self, message: Message):
        self.ltm.store(message)

    def get_context(self, query, max_results=3):
        return self.wm.retrieve(query, max_results)

    def clear_all(self):
        self.stm.clear()
        self.ltm.clear()
