# tools/archivage_tool.py

from skills.communication.messages import Message
from skills.memory.long_term import LongTermMemory

class ArchivageTool:
    def __init__(self, agent, db_path="long_term_archive.db", verbose=False):
        self.agent = agent
        self.verbose = verbose
        self.memory = LongTermMemory(db_path=db_path, verbose=verbose)

    def handle_message(self, message: Message, agent=None):
        agent = agent or self.agent

        if not isinstance(message, Message):
            raise ValueError("ArchivageTool attend un objet Message valide.")

        self.memory.save(message)

        if self.verbose:
            print(f"[{agent.name}] [ArchivageTool] Message archivé dans {self.memory.db_path}")

        return Message(
            origine=agent.name,
            destinataire=message.origine,
            type_message="confirmation",
            contenu="Message archivé avec succès.",
            meta={},
            conversation_id=message.conversation_id or message.id
        )
