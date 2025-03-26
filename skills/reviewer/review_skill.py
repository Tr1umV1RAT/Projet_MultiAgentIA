import re
from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_wrapper import LLMWrapper

class ReviewSkill(BaseSkill):
    """
    Skill permettant à l'agent de relire du code et de formuler une évaluation claire.
    Peut être utilisé par un reviewer pour détecter erreurs, mauvaises pratiques ou manques de clarté.
    """
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose
        self.llm = LLMWrapper(agent=agent, verbose=verbose)

    def handle_message(self, message: Message, agent=None):
        agent = agent or self.agent

        if message.type_message != "code":
            return None

        if self.verbose:
            print(f"[{agent.name}] [ReviewSkill] Analyse d’un message de type code...")

        prompt = (
            f"{agent.get_prompt_context()}\n\n"
            "Voici un fichier de code à relire et commenter :\n"
            "Analyse la qualité du code, signale les erreurs potentielles, "
            "propose des améliorations si nécessaire.\n\n"
            f"{message.contenu}"
        )

        response_msg = self.llm.ask(
            prompt,
            meta={"skill": "ReviewSkill", "cible": message.origine}
        )

        response_msg.destinataire = message.origine
        response_msg.type_message = "review"
        response_msg.meta["filename"] = message.meta.get("filename", "")
        response_msg.conversation_id = message.conversation_id or message.id

        return response_msg
