from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from tools.llm_wrapper import LLMWrapper

class SyntheseSkill(BaseSkill):
    """
    Skill permettant de résumer les échanges ou les informations échangées entre les agents.
    Peut être déclenché après une revue de code, un plan, ou toute interaction importante.
    """
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose
        self.llm = LLMWrapper(agent=agent, verbose=verbose)

    def handle_message(self, message: Message, agent=None):
        agent = agent or self.agent

        # On ne résume que des messages importants ou explicites
        if not message.dialogue and message.type_message not in {"review", "code", "system"}:
            return None

        if self.verbose:
            print(f"[{agent.name}] [SyntheseSkill] Traitement d’un message pour synthèse...")

        # Construction du prompt pour le LLM
        prompt = (
            f"{agent.get_prompt_context()}\n\n"
            "Voici un extrait d’interaction entre agents dans un projet de développement :\n\n"
            f"{message.contenu}\n\n"
            "Résume les points essentiels, décisions prises, recommandations ou problèmes détectés. "
            "Le résumé doit être clair, synthétique, et orienté vers l’action."
        )

        response = self.llm.ask(
            prompt,
            meta={"skill": "SyntheseSkill", "source": message.origine}
        )

        # Adaptation du message généré
        response.destinataire = "ALL"
        response.type_message = "synthese"
        response.dialogue = True
        response.meta["origine_resume"] = message.origine
        response.meta["resume_de"] = message.type_message
        response.conversation_id = message.conversation_id or message.id

        return response
