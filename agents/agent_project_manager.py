# agents/agent_project_manager.py

import os
from datetime import datetime

from agents.base_agent import BaseAgent
from skills.project_synthesis_skill import SkillProjectSynthesis
from skills.communication.messages import Message

class AgentProjectManager(BaseAgent):
    def __init__(self, name="ProjectManager", role=None, base_path="project_outputs", verbose=False):
        super().__init__(name=name, role=role, verbose=verbose)

        # Initialisation du répertoire de projet
        self.project_name = f"projet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.project_path = os.path.join(base_path, self.project_name)
        os.makedirs(self.project_path, exist_ok=True)

        # Instanciation de la skill de synthèse
        self.synth_skill = SkillProjectSynthesis(
            agent=self,
            project_path=self.project_path,
            memory=self.memory,
            verbose=verbose
        )
        self.skills.append(self.synth_skill)

        if self.verbose:
            print(f"[ProjectManager] Projet initialisé : {self.project_name}")

    def transmit_to_design_manager(self, objectif, destinataire="DesignManager"):
        message = Message(
            origine=self.name,
            destinataire=destinataire,
            contenu=objectif,
            metadata={"action": "plan"}
        )
        self.communication.send(message)
        self.memory.store_message(message)
        return message

    def synthesize_round(self, destinataire="Utilisateur"):
        contenu = self.synth_skill.generate_synthesis()
        msg = Message(
            origine=self.name,
            destinataire=destinataire,
            contenu=contenu,
            metadata={"type": "synthese"}
        )
        self.communication.send(msg)
        self.memory.store_message(msg)
        return msg

    def receive_message(self, message):
        if message.contenu.strip().lower() == "synthese":
            return self.synthesize_round(destinataire=message.origine)
        return super().receive_message(message)