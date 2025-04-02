from agents.base_agent import BaseAgent
from skills.coder_skill import SkillCoder
from skills.planning_skill import SkillPlanning
from roles.team_codeur_role import RoleTeamCodeur

role_map = {
    "role_codeur": RoleTeamCodeur,
    # autres rôles
}

skill_map = {
    "coder": SkillCoder,
    "plan": SkillPlanning,
    # autres skills
}

class AgentFactory:
    @staticmethod
    def create(name, role=None, skills=None, verbose=True):
        role_instance = role_map[role]() if role else None
        agent = BaseAgent(name=name, role=role_instance, verbose=verbose)

        for skill_name in skills:
            skill_cls = skill_map.get(skill_name)
            if skill_cls:
                skill_instance = skill_cls(agent=agent, memory=agent.memory)
                agent.skills.append(skill_instance)

        return agent
