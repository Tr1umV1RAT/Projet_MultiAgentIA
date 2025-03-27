# skills/planning/skill_planner.py

from typing import Optional
from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from skills.memory.memory_manager import MemoryManagerTool

class SkillPlanner(BaseSkill):
    def __init__(self, agent, verbose=False):
        self.agent = agent
        self.verbose = verbose
        self.memory: Optional[MemoryManagerTool] = None
        self.skill_manager: Optional[SkillManagerTool] = None

    def _get_tool(self, tool_name: str):
        for tool in getattr(self.agent, "tools", []):
            if tool.__class__.__name__ == tool_name:
                return tool
        return None

    def handle_message(self, message: Message, agent=None) -> Message:
        agent = agent or self.agent

        if not self.memory:
            self.memory = self._get_tool("MemoryManagerTool")
        if not self.skill_manager:
            self.skill_manager = self._get_tool("SkillManagerTool")

        if self.verbose:
            print(f"[{agent.name}] [SkillPlanner] Analyse du message : {message}")
            print(f"Contenu : {message.contenu}")

        available_skills = {name.lower() for name in self.skill_manager.list_skills()} if self.skill_manager else set()
        available_tools = {type(tool).__name__.lower(): tool for tool in getattr(agent.role, "outils", [])}

        plan = []
        content_lower = message.contenu.lower()

        if "reasoningskill" in available_skills and message.type_message in ["task", "instruction"]:
            plan.append({
                "type": "skill",
                "name": "ReasoningSkill",
                "objectif": "Produire une réponse textuelle"
            })

        if "codepostprocessorskill" in available_skills and (
            "```python" in message.contenu or
            "def " in message.contenu or
            "class " in message.contenu or
            content_lower.strip().endswith(".py")
        ):
            plan.append({
                "type": "skill",
                "name": "CodePostProcessorSkill",
                "objectif": "Extraire et sauvegarder le code généré"
            })

        if "dbmanagementskill" in available_skills and message.memoriser and self.memory:
            self.memory.save_to_long_term(message)
            plan.append({
                "type": "skill",
                "name": "DBManagementSkill",
                "objectif": "Archiver le message dans la base"
            })

        if self.verbose:
            print(f"[DEBUG] 📤 Plan envoyé dans le message : {plan}")

        return Message.system(
            expediteur=agent.name,
            destinataire=agent.name,
            contenu="Planification dynamique effectuée.",
            meta={"plan": plan},
            conversation_id=message.conversation_id or message.id
        )