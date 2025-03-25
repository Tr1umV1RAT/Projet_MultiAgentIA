# skills/planning/plan_executor.py

from typing import Optional
from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class PlanExecutorSkill(BaseSkill):
    def __init__(self, agent, verbose: bool = False):
        self.agent = agent
        self.verbose = verbose

    def handle_message(self, message: Message, agent=None) -> Optional[Message]:
        agent = agent or self.agent

        if message.type_message != "system" or "plan" not in message.meta:
            if self.verbose:
                print(f"[{agent.name}] [PlanExecutor] Aucun plan trouvé dans le message.")
            return None

        plan = message.meta["plan"]
        if not plan:
            if self.verbose:
                print("[DEBUG] ⚠️ Plan vide ou non trouvé.")
            return None

        results = []

        if self.verbose:
            print(f"[{agent.name}] [PlanExecutor] Exécution du plan : {plan}")

        for step in plan:
            type_element = step.get("type", "skill")  # fallback si ancien plan
            name = step.get("name")
            objectif = step.get("objectif")

            if type_element == "skill":
                cible = self._get_skill(name)
            elif type_element == "tool":
                cible = self._get_tool(name)
            else:
                cible = None

            if cible and hasattr(cible, "handle_message"):
                result = cible.handle_message(message, agent=agent)
                results.append(result)
                if self.verbose:
                    print(f"[{agent.name}] [PlanExecutor] {type_element.capitalize()} {name} exécuté pour : {objectif}")
            else:
                if self.verbose:
                    print(f"[{agent.name}] [PlanExecutor] {type_element.capitalize()} {name} introuvable ou invalide.")

        return Message(
            origine=agent.name,
            destinataire=message.origine,
            type_message="resultats_plan",
            contenu=f"{len(results)} étapes du plan exécutées.",
            meta={"resultats": [r.to_dict() for r in results if r]},
            conversation_id=message.conversation_id or message.id
        )

    def _get_skill(self, name):
        for skill in getattr(self.agent, "skills", []):
            if type(skill).__name__ == name:
                return skill
        return None

    def _get_tool(self, name):
        outils = getattr(self.agent.role, "outils", [])
        for tool in outils:
            if type(tool).__name__ == name:
                return tool
        return None
