import argparse
import os
import shutil
from skills.memory.long_term import LongTermMemory
from skills.communication.messages import Message
from utils.memory_display import print_agent_memory


def find_latest_memory_dir(agent_name: str, base_dir: str) -> str:
    """
    Retourne le dossier mémoire le plus récent pour un agent donné.
    """
    candidates = sorted(
        [d for d in os.listdir(base_dir) if d.startswith(agent_name)],
        reverse=True
    )
    if not candidates:
        raise FileNotFoundError(f"Aucun dossier mémoire trouvé pour l’agent {agent_name}")
    return os.path.join(base_dir, candidates[0])


def show_memory(agent_name, memory_path, limit, type_msg, min_importance):
    mem = LongTermMemory(agent_name, memory_path)
    entries = mem.fetch(
        type_message=type_msg,
        min_importance=min_importance,
        limit=limit
    )
    print_agent_memory(agent_name, entries)


def delete_memory_dir(memory_path):
    if os.path.exists(memory_path):
        confirmation = input(f"⚠️ Supprimer définitivement le dossier : {memory_path} ? (y/N) ")
        if confirmation.lower() == 'y':
            shutil.rmtree(memory_path)
            print("✅ Dossier supprimé.")
        else:
            print("❌ Annulé.")
    else:
        print(f"⚠️ Dossier introuvable : {memory_path}")


def main():
    parser = argparse.ArgumentParser(description="🧠 Outil mémoire agent : affichage ou suppression.")
    parser.add_argument("agent", type=str, help="Nom de l'agent (ex: Codeur)")
    parser.add_argument("--base", type=str, default="/mnt/data/agent_memories", help="Dossier des mémoires")
    parser.add_argument("--limit", type=int, default=30, help="Nombre maximum de souvenirs à afficher")
    parser.add_argument("--type", type=str, default=None, help="Filtrer par type de message (code, erreur, etc.)")
    parser.add_argument("--min_importance", type=int, default=2, help="Filtrer par importance minimale")
    parser.add_argument("--show", action="store_true", help="Afficher la mémoire (par défaut)")
    parser.add_argument("--delete", action="store_true", help="Supprimer le dossier mémoire le plus récent")

    args = parser.parse_args()

    try:
        memory_path = find_latest_memory_dir(args.agent, args.base)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    print(f"📁 Dossier mémoire sélectionné : {memory_path}")

    if args.delete:
        delete_memory_dir(memory_path)
    else:
        show_memory(args.agent, memory_path, args.limit, args.type, args.min_importance)


if __name__ == "__main__":
    main()
