from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_wrapper import LLMWrapper  # ✅ import désormais explicite

class PlanificationSkill(BaseSkill):
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose
        self.llm = LLMWrapper(agent=agent, verbose=verbose)

    def handle_message(self, message: Message, agent=None):
        agent = agent or self.agent

        if message.type_message != "system":
            return None

        if self.verbose:
            print(f"[{agent.name}] [PlanificationSkill] Analyse du message initial...")

        # Construction du prompt
        prompt = (
            f"{agent.get_prompt_context()}\n\n"
            f"Voici la consigne à planifier :\n{message.contenu}\n\n"
            "Propose un plan d’action structuré en étapes claires à déléguer à chaque membre de l’équipe. "
            "Indique à qui déléguer chaque tâche."
        )

        # ✅ Appel propre au LLM via le wrapper
        response_msg = self.llm.ask(prompt, meta={"skill": "PlanificationSkill"})

        if self.verbose:
            print(f"[{agent.name}] [PlanificationSkill] Plan généré :\n{response_msg.contenu}")

        # Adaptation du message en sortie
        response_msg.destinataire = "ALL"
        response_msg.type_message = "system"
        response_msg.meta["planifie"] = True
        response_msg.dialogue = True

        return response_msg
