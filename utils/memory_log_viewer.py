import argparse
import sqlite3
import json
import os
from datetime import datetime


DEFAULT_DB = "/mnt/data/memory_access_log.db"


def main():
    parser = argparse.ArgumentParser(description="🕵️ Affiche les accès inter-agent à la mémoire.")
    parser.add_argument("--db", type=str, default=DEFAULT_DB, help="Chemin vers memory_access_log.db")
    parser.add_argument("--limit", type=int, default=30, help="Nombre de lignes à afficher")
    parser.add_argument("--filter-agent", type=str, help="Filtrer par nom de l'agent ciblé")
    parser.add_argument("--filter-requester", type=str, help="Filtrer par nom du demandeur")
    parser.add_argument("--since", type=str, help="Filtrer les accès après une date (ex: 2025-03-26T04:30)")

    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"❌ Base introuvable : {args.db}")
        return

    try:
        since_dt = datetime.fromisoformat(args.since) if args.since else None
    except Exception as e:
        print(f"❌ Format de date invalide pour --since : {e}")
        return

    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()

    query = "SELECT timestamp, requester, target_agent, action, meta FROM memory_access_log WHERE 1=1"
    params = []

    if args.filter_agent:
        query += " AND target_agent = ?"
        params.append(args.filter_agent)
    if args.filter_requester:
        query += " AND requester = ?"
        params.append(args.filter_requester)
    if since_dt:
        query += " AND timestamp >= ?"
        params.append(since_dt.isoformat())

    query += " ORDER BY id DESC LIMIT ?"
    params.append(args.limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    print(f"\n📜 Journal des accès mémoire ({len(rows)} lignes)\n" + "-"*60)
    for row in rows:
        timestamp, requester, target, action, meta = row
        try:
            meta_obj = json.loads(meta)
        except:
            meta_obj = meta
        print(f"🕒 [{timestamp}] {requester} ➜ {target} | {action} | meta={meta_obj}")


if __name__ == "__main__":
    main()
