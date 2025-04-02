# run_code_team.py

from teams.code_team import CodeTeam
import os

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Lancer un round de la CodeTeam")
    parser.add_argument("objectif", type=str, nargs="?", help="Objectif du projet à coder")
    parser.add_argument("--verbose", action="store_true", help="Afficher les messages internes")
    parser.add_argument("--increment", type=str, help="Reprendre un projet existant depuis un dossier")

    args = parser.parse_args()

    if args.increment:
        # Chargement depuis un état précédent
        state_path = os.path.join(args.increment, "state", "project_state.json")
        team = CodeTeam.from_saved_state(state_path, verbose=args.verbose)
        objectif = team.history[0].contenu if team.history else "Continuer le projet"
        print(f"\n=== Reprise d'un projet existant ===")
    elif args.objectif:
        team = CodeTeam(verbose=args.verbose)
        objectif = args.objectif
        print("\n=== Lancement d'un nouveau round de la CodeTeam ===")
    else:
        raise ValueError("Vous devez fournir soit un objectif, soit --increment dossier_projet")

    print(f"🎯 Objectif : {objectif}\n")

    team.run_round(objectif)

    print("\n=== Historique des messages échangés ===")
    for msg in team.history:
        print(f"[{msg.origine} → {msg.destinataire}]\n{msg.contenu}\n")
