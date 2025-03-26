# skills/reasoning.py

from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_interface import LLMInterface

class Reasoning(BaseSkill):
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose

    def handle_message(self, message: Message, agent=None) -> Message:
        agent = agent or self.agent

        if not message.is_valid():
            raise ValueError(f"[{agent.name}] Message invalide reçu dans ReasoningSkill.")

        if self.verbose:
            print(f"[{agent.name}] [REASONING] Traitement du message reçu : {message}")

        prompt = agent.role.get_prompt(message)

        llm_tool: LLMInterface = self._get_llm_tool_from_role(agent.role)
        if llm_tool is None:
            raise RuntimeError(f"[{agent.name}] Aucun outil LLM trouvé dans le rôle {agent.role.name}")

        response_text = llm_tool.query(prompt)

        if self.verbose:
            print(f"[{agent.name}] [REASONING] Réponse générée :\n{response_text}\n")

        response_msg = Message(
            origine=agent.name,
            destinataire=message.origine,
            type_message="reponse",
            contenu=response_text,
            meta={"source_message_id": message.id, "prompt": prompt},
            conversation_id=message.conversation_id or message.id
        )

        return response_msg

    def _get_llm_tool_from_role(self, role):
        for outil in role.outils:
            if isinstance(outil, LLMInterface):
                return outil
        return None
