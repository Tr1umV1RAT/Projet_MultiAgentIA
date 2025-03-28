from skills.communication import Communication
from skills.memory.memory_manager import MemoryManager
from skills.memory.memory_retriever import MemoryRetrieverSkill
from tools.llm_interface import LLMInterface
from skills.communication.messages import Message
from skills.memory.short_term_memory import ShortTermMemory
from skills.memory.long_term_memory import LongTermMemory
from skills.memory.working_memory import WorkingMemory



class BaseAgent:
    def __init__(self, name, role, skills=None, verbose=False, communication=None, llm=None, memory_enabled=True, base_path="agent_memories"):
        self.name = name
        self.role = role
        self.verbose = verbose
        self.llm = llm if llm else LLMInterface(agent=self, verbose=verbose)       
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory(db_path=f"{base_path}/{self.name}_ltm.db")
        self.wm = WorkingMemory(self.llm, self.ltm)
        self.memory = MemoryManager(self.stm, self.ltm, self.wm) if memory_enabled else None
        self.communication = communication if communication else Communication(verbose=verbose)
        self.messages = []
        self.retriever = MemoryRetrieverSkill(self,self.ltm,llm)
        self.skills = skills if skills else []
        self.skills += self.init_default_skills()

    def init_default_skills(self):
        default_skills = [self.communication, self.retriever]
        if self.memory:
            default_skills.append(self.memory)
        return default_skills

    def init_memory(self, base_path="agent_memories"):
        """Initialise automatiquement les mémoires (STM, LTM, WorkingMemory)."""
        stm = ShortTermMemory()
        ltm = LongTermMemory(db_path=f"{base_path}/{self.name}_ltm.db")
        wm = WorkingMemory(self.llm, ltm)
        self.memory = MemoryManager(stm, ltm, wm)

        if self.verbose:
            print(f"[Memory] Mémoire activée pour {self.name}.")

    def receive_message(self, message: Message):
        """Ajoute un message à la file d'attente."""
        self.messages.append(message)
        if self.verbose:
            print(f"[{self.name}] Message reçu : {message}")

    def process_messages(self):
        while self.messages:
            message = self.messages.pop(0)
            if self.memory and message.memoriser:
                self.memory.store_message(message)
                contexte = self.retriever.build_retrieval_prompt(message) if self.memory else ""
            prompt_final = f"{self.role.get_prompt(message)}\nContexte: {contexte}\n{message.contenu}"
            response_contenu = self.llm.query(prompt_final)

            response_msg = Message(
                origine=self.name,
                destinataire=message.origine,
                type_message="llm_response",
                contenu=response_contenu,
                dialogue=True,
                memoriser=True,
                metadata={"reponse_a": getattr(message, 'id', None)}
            )

            if self.memory:
                self.memory.store_message(response_msg)
            self.communication.send(response_msg)

    def get_prompt_context(self, message: Message):
        """Retourne le prompt de rôle pour initialiser ou enrichir le contexte."""
        if self.messages:
            message = self.messages.pop(0) 
        return self.role.get_prompt(Message or message_recu)

    @property
    def objectif(self):
        return getattr(self.role, "objectif", None)

    def __repr__(self):
        return f"<Agent {self.name} - Rôle: {self.role.name}>"

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:])

    if not prompt:
        print("Veuillez fournir un prompt.")
        sys.exit(1)

    from roles.base_role import BaseRole
    role = BaseRole(name="DefaultAgent", objectif="Conversation générale")
    agent = BaseAgent(name="AgentCLI", role=role)

    message_recu = Message(contenu=prompt, origine="user", destinataire="AgentCLI")
    agent.receive_message(message_recu)
    agent.process_messages()