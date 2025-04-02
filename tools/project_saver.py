# tools/project_saver.py

import os
import json
from datetime import datetime
from skills.communication.messages import Message

def save_project_state(team, output_dir):
    """
    Sauvegarde l'état courant d'une équipe de projet (agents, historique, chemins mémoire).
    """
    os.makedirs(output_dir, exist_ok=True)
    state_path = os.path.join(output_dir, "project_state.json")

    state = {
        "team_name": team.name,
        "project_path": team.project_path,
        "agents": {},
        "history": [],
        "timestamp": datetime.now().isoformat()
    }

    for name, agent in team.agents.items():
        state["agents"][name] = {
            "role": agent.role.name if agent.role else None,
            "ltm_path": agent.memory.ltm.path if hasattr(agent.memory, "ltm") else None
        }

    for msg in team.history:
        state["history"].append({
            "origine": msg.origine,
            "destinataire": msg.destinataire,
            "contenu": msg.contenu,
            "metadata": msg.metadata,
            "conversation_id": msg.conversation_id
        })

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    if team.verbose:
        print(f"[ProjectSaver] État du projet sauvegardé dans : {state_path}")

    return state_path

def load_project_state(filepath):
    """
    Charge un projet sauvegardé depuis un fichier JSON
    et retourne une structure {name, project_path, agents, history}.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        state = json.load(f)

    state["history"] = [
        Message(
            origine=m["origine"],
            destinataire=m["destinataire"],
            contenu=m["contenu"],
            conversation_id=m.get("conversation_id"),
            metadata=m.get("metadata", {})
        ) for m in state.get("history", [])
    ]

    return state