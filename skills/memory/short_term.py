from skills.base_skill import BaseSkill

class ShortTermMemory(BaseSkill):
    def __init__(self):
        super().__init__("ShortTermMemory")
        # Stocke des informations générales
        self.memoires = []
        # Stocke l'historique des messages de la conversation
        self.messages = []

    def save(self, contenu, agent_name=None, type_info=None):
        """Sauvegarde une information générale dans la mémoire."""
        self.memoires.append({
            "agent_name": agent_name,
            "type_info": type_info,
            "contenu": contenu
        })

    def recall(self, agent_name=None, type_info=None, limit=10):
        """Récupère les dernières informations correspondant aux filtres donnés."""
        resultats = [
            m for m in self.memoires
            if (agent_name is None or m["agent_name"] == agent_name) and
               (type_info is None or m["type_info"] == type_info)
        ]
        return resultats[-limit:]

    def add_message(self, message: str):
        """Ajoute un message à l'historique de la conversation."""
        self.messages.append(message)
    
    def get_recent_history(self, limit=3) -> str:
        """Retourne les derniers messages sous forme d'une chaîne séparée par des sauts de ligne."""
        return "\n".join(self.messages[-limit:]) if self.messages else ""
    
    def execute(self):
        """Implémentation minimale de la méthode abstraite 'execute' de BaseSkill."""
        pass
