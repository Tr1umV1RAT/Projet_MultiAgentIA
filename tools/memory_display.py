from skills.communication.messages import Message

def print_agent_memory(agent_name: str, entries: list, max_len: int = 120):
    """
    Affiche joliment la mémoire d’un agent à partir d’une liste d’entrées.
    Chaque entrée doit être un dict avec :
        - "timestamp"
        - "role"
        - "content" : soit un objet Message, soit une string/dict
    """
    print(f"\n🧠 Mémoire de l’agent {agent_name} :\n" + "-"*60)

    if not entries:
        print("⚠️ Aucun souvenir trouvé.")
        return

    for entry in entries:
        contenu = entry["content"]
        if isinstance(contenu, Message):
            print(f"📌 [{contenu.date:%H:%M:%S}] {contenu.origine} ➜ {contenu.destinataire} ({contenu.type_message})")
            print(f"    {contenu.contenu.strip()[:max_len]}")
        elif isinstance(contenu, dict):
            print(f"📁 {entry['timestamp']} - [DICT] {contenu.get('origine', '?')} ➜ {contenu.get('destinataire', '?')}")
            print(f"    {str(contenu.get('contenu', ''))[:max_len]}")
        else:
            print(f"💤 {entry['timestamp']} - [RAW] {str(contenu)[:max_len]}")
