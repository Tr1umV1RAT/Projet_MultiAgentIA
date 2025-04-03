# skills/skill_manager.py

from config import Config

class SkillManager:
    def __init__(self, agent, available_skills=None):
        self.agent = agent
        self.available_skills = available_skills or {}
        self.active_skills = set()

    def add_skill(self, skill_name, skill_instance):
        self.available_skills[skill_name] = skill_instance
        if Config.verbose:
            print(f"[SkillManager][{self.agent.name}] Skill '{skill_name}' ajouté.")

    def activate_skill(self, skill_name):
        if skill_name in self.available_skills:
            self.active_skills.add(skill_name)
            if Config.verbose:
                print(f"[SkillManager][{self.agent.name}] Skill '{skill_name}' activé.")
        elif Config.verbose:
            print(f"[SkillManager][{self.agent.name}] Impossible d'activer '{skill_name}' (non trouvé).")

    def deactivate_skill(self, skill_name):
        if skill_name in self.active_skills:
            self.active_skills.discard(skill_name)
            if Config.verbose:
                print(f"[SkillManager][{self.agent.name}] Skill '{skill_name}' désactivé.")
        elif Config.verbose:
            print(f"[SkillManager][{self.agent.name}] Impossible de désactiver '{skill_name}' (déjà inactif).")

    def run_skill(self, skill_name, message):
        if skill_name in self.active_skills:
            skill = self.available_skills[skill_name]
            if Config.verbose:
                print(f"[SkillManager][{self.agent.name}] Exécution du skill '{skill_name}' (Message ID : {message.id}).")
            return skill.execute(message)
        elif Config.verbose:
            print(f"[SkillManager][{self.agent.name}] Skill '{skill_name}' inactif ou inexistant.")
        return None

    def handle_message(self, message):
        # Activer ou désactiver dynamiquement selon les métadonnées
        activate = message.metadata.get('activate_skill')
        deactivate = message.metadata.get('deactivate_skill')
        skill_to_run = message.metadata.get('skill')

        if activate:
            self.activate_skill(activate)

        if deactivate:
            self.deactivate_skill(deactivate)

        if skill_to_run:
            return self.run_skill(skill_to_run, message)

        elif Config.verbose:
            print(f"[SkillManager][{self.agent.name}] Aucun skill spécifié explicitement dans le message (Message ID : {message.id}).")
        return None
