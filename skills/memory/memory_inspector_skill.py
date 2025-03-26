from skills.base_skill import BaseSkill
from skills.communication.messages import Message

class MemoryInspectorSkill(BaseSkill):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def handle_message(self, message: Message, agent):
        if message.action != "inspect_memory":
            return None  # pas concerné

        filtre_type = message.meta.get("type")
        min_importance = message.meta.get("min_importance", 2)
        afficher_contenu = message.meta.get("afficher_contenu", True)

        # Récupération depuis la mémoire longue
        entries = agent.memoire.long_term.fetch(
            type_message=filtre_type,
            min_importance=min_importance
        )

        if not entries:
            return Message.system("MemoryInspector", agent.name, "Aucun souvenir correspondant.")

        texte = ""
        for e in entries:
            if afficher_contenu:
                texte += f"- ({e['timestamp']}) {e['role']} : {e['content']}\n"
            else:
                texte += f"- ({e['timestamp']}) {e['role']} (contenu masqué)\n"

        return Message(
            origine="MemoryInspector",
            destinataire=agent.name,
            type_message="memoire",
            contenu=f"Résumé mémoire ({len(entries)} entrées) :\n\n{texte}",
            importance=5
        )