# tools/llm_wrapper.py

from skills.communication.messages import Message
from tools.llm_adapter import LLMAdapterTool

class LLMWrapper:
    def __init__(self, agent, verbose: bool = False):
        self.agent = agent
        self.verbose = verbose
        self.llm = LLMAdapterTool(agent)

    def ask(self, prompt: str, meta: dict = None, system_prompt: str = None) -> Message:
        meta = meta or {}
        full_prompt = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"

        if self.verbose:
            print(f"[{self.agent.name}] [LLMWrapper] Prompt envoyé :\n{full_prompt}\n")

        response = self.llm.query(full_prompt)

        return Message(
            origine=self.agent.name,
            destinataire=self.agent.name,
            type_message="llm_response",
            contenu=response,
            meta=meta
        )
