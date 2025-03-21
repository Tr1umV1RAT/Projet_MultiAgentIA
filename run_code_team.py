import argparse
from teams.code_team import CodeTeam

def main():
    parser = argparse.ArgumentParser(description="Lancer une équipe de codage IA.")
    parser.add_argument("objectif", type=str, help="Objectif de l'équipe de code (ex: 'Crée un jeu de stratégie')")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds d’interaction (par défaut : 5)")
    parser.add_argument("--name", type=str, default=None, help="Nom du projet (facultatif)")
    parser.add_argument("--no-review", action="store_true", help="Désactive le reviewer")
    parser.add_argument("--overwrite_db", action="store_true", help="Écrase la base si elle existe")

    args = parser.parse_args()

    nom_projet = args.name if args.name else "CodeTeamProject"
    team = CodeTeam(
        nom_projet=nom_projet,
        objectif=args.objectif,
        n_rounds=args.n_round,
        use_reviewer=not args.no_review,
        overwrite_db=args.overwrite_db
    )

    team.run()
    team.cloturer()

if __name__ == "__main__":
    main()
