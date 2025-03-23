from tools.llm_adapter import LLMAdapterTool
from skills.communication.messages import Message

class Reasoning:
    def __init__(self, agent):
        """
        Initialise la compétence de raisonnement pour un agent.
        L'agent est utilisé pour accéder à son rôle et à sa mémoire pour enrichir le prompt.
        """
        self.agent = agent
        self.llm_tool = LLMAdapterTool()

    def reflechir(self, input_message: Message) -> Message:
        # Utilise le prompt de base à partir du rôle de l'agent
        if hasattr(self.agent, 'role') and self.agent.role is not None:
            base_prompt = self.agent.role.generer_prompt(input_message.contenu)
            extended_context = ""
            if hasattr(self.agent.role, 'get_extended_context') and callable(self.agent.role.get_extended_context):
                extended_context = self.agent.role.get_extended_context()
            prompt = f"{base_prompt}\n" + (f"Contexte étendu:\n{extended_context}\n" if extended_context else "")
        else:
            prompt = input_message.contenu

        # Ajouter l'historique récent (augmenté de la part globale si besoin)
        if hasattr(self.agent, 'memoire') and callable(getattr(self.agent.memoire, 'get_recent_history', None)):
            recent_history = self.agent.memoire.get_recent_history(limit=5)
            if recent_history:
                prompt = f"{prompt}\nHistorique récent:\n{recent_history}\n"

        response_text = self.llm_tool.run(prompt)
        response_message = Message.create(
            expediteur=self.agent.name,
            destinataire=input_message.expediteur,  # On envoie la réponse à l'expéditeur initial.
            contenu=response_text,
            dialogue=True,
            meta={"original_prompt": prompt}
        )
        return response_message