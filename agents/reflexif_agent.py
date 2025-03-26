# agents/reflexif_agent.py

from agents.base_agent import BaseAgent
from skills.communication.messages import Message

class AgentReflexif(BaseAgent):
    def __init__(self, name, role, verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

    def activate(self, message: Message):
        if self.verbose:
            print(f"[{self.name}] Activation sur message : {message}")

        # Contexte du rôle
        system_prompt = self.get_prompt_context()

        # Requête au LLM
        response = self.llm.ask(
            prompt=message.contenu,
            system_prompt=system_prompt,
            meta={"source": message.origine}
        )

        if self.verbose:
            print(f"[{self.name}] Réponse générée : {response.contenu}")

        return response