from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_interface import LLMInterface  # à adapter si renommé
from skills.communication.prompt_builder import PromptBuilder

class LLMSkill(BaseSkill):
    def __init__(self, agent_name, role=None, memory=None, prompt_builder=None):
        super().__init__(agent_name)
        self.role = role
        self.memory = memory  # MemoryRetrieverSkill ou autre
        self.prompt_builder = prompt_builder or PromptBuilder()

    def retrieve_context(self, message: Message) -> str:
        """
        Optionnellement surchargeable.
        Récupère du contexte pertinent depuis la mémoire.
        """
        if self.memory:
            return self.memory.retrieve(message)
        return ""

    def build_prompt(self, message: Message, context: str) -> str:
        """
        Fabrique un prompt structuré via le PromptBuilder ou surchargé manuellement.
        """
        return self.prompt_builder.build_prompt(
            intro=self.role or "Tu es un assistant intelligent.",
            task=message.content,
            memory=context,
            constraints=message.metadata.get("constraints", [])
        )

    def call_llm(self, prompt: str) -> str:
        return LLMInterface.query(prompt)

    def format_output(self, llm_output: str, original_message: Message) -> Message:
        """
        Par défaut, renvoie un Message contenant le texte généré.
        Peut être surchargé.
        """
        return Message(
            role=self.agent_name,
            content=llm_output,
            type="text",
            metadata={"response_to": original_message.id}
        )

    def execute(self, message: Message) -> Message:
        context = self.retrieve_context(message)
        prompt = self.build_prompt(message, context)
        llm_response = self.call_llm(prompt)
        return self.format_output(llm_response, message)
