# tools/skill_manager.py
class SkillManagerTool:
    def __init__(self, agent):
        self.agent = agent



    def list_skills(self):
        return [type(skill).__name__ for skill in getattr(self.agent, "skills", [])]

    def get_skill(self, skill_name: str):
        for skill in getattr(self.agent, "skills", []):
            if type(skill).__name__ == skill_name:
                return skill
                
        return None

    def execute_skill(self, skill_name: str, message):
        skill = self.get_skill(skill_name)
        if skill is None:
            raise ValueError(f"Skill '{skill_name}' introuvable pour l'agent {self.agent.name}.")
        if not hasattr(skill, "handle_message"):
            raise TypeError(f"Skill '{skill_name}' n'a pas de méthode handle_message.")
        print(f"[DEBUG] 📤 Plan envoyé dans le message : {plan}")
        return skill.handle_message(message, agent=self.agent)
