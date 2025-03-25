# skills/reasoning.py
from tools.llm_adapter import LLMAdapterTool
from skills.communication.messages import Message
from skills.base_skill import BaseSkill


class Reasoning(BaseSkill):
    def __init__(self, agent, adapter, verbose=False):
        super().__init__(agent=agent, verbose=verbose)
        self.adapter = adapter

    def reflechir(self, input_message):
        historique = ""
        if hasattr(self.agent, 'memoire'):
            historique = self.agent.memoire.get_recent_history()
        prompt = self.agent.role.generer_prompt() + "\n" + historique + "\n" + input_message.contenu

        if hasattr(input_message, 'meta') and input_message.meta and "action" in input_message.meta:
            action = input_message.meta["action"]
            for outil in getattr(self.agent.role, "outils", []):
                if outil.__class__.__name__.lower().startswith(action.lower()):
                    resultat = outil.run(input_message.contenu)
                    prompt += f"\nRésultat de {outil.__class__.__name__}: {resultat}"
                    break

        reponse = self.adapter.run(prompt)
        return reponse

    def execute(self, input_message):
        return self.reflechir(input_message)
