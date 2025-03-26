from skills.base_skill import BaseSkill
from skills.communication.messages import Message


class MemoryInspectorSkill(BaseSkill):
    """
    Skill permettant à un agent d’analyser sa propre mémoire longue.
    Peut :
    - Filtrer les souvenirs selon des critères (type, importance, etc.)
    - Résumer les points clés via un appel au LLM
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def handle_message(self, message: Message, agent):
        if message.action != "inspect_memory":
            return None  # pas concerné

        filtre_type = message.meta.get("type")
        min_importance = message.meta.get("min_importance", 2)
        afficher_contenu = message.meta.get("afficher_contenu", False)
        resume_llm = message.meta.get("resume_intelligent", False)
        max_entries = message.meta.get("limit", 50)

        # Accès à la mémoire longue via l’agent
        entries = agent.memoire.long_term.fetch(
            type_message=filtre_type,
            min_importance=min_importance,
            limit=max_entries
        )

        if not entries:
            return Message.system("MemoryInspector", agent.name, "Mémoire vide ou aucun souvenir filtré.")

        if resume_llm:
            # Construit un corpus brut
            contenu = "\n".join(f"{e['content']}" for e in entries)

            prompt = f"""Tu es un assistant IA qui aide un agent à faire le point sur ses souvenirs.
Voici les extraits de mémoire :
---
{contenu}
---

Identifie les éléments importants, les thèmes récurrents, et les potentielles informations sensibles.
"""

            if hasattr(agent.llm, "ask"):
                resultat = agent.llm.ask(prompt)
                texte = getattr(resultat, "contenu", str(resultat))
            elif hasattr(agent.llm, "query"):
                texte = agent.llm.query(prompt)
            else:
                texte = "[ERREUR: LLM incompatible]"

            return Message(
                origine="MemoryInspector",
                destinataire=agent.name,
                type_message="memoire",
                contenu=texte,
                importance=7
            )

        else:
            # Mode brut (listing)
            texte = ""
            for e in entries:
                if afficher_contenu:
                    texte += f"- ({e['timestamp']}) {e['role']} : {e['content']}\n"
                else:
                    texte += f"- ({e['timestamp']}) {e['role']}\n"

            return Message(
                origine="MemoryInspector",
                destinataire=agent.name,
                type_message="memoire",
                contenu=f"Souvenirs (filtrés) :\n\n{texte}",
                importance=3
            )