# cli/run_code_team.py
import argparse
from teams.code_team import CodeTeam

parser = argparse.ArgumentParser(description="Lancer une CodeTeam IA pour générer un projet logiciel.")

parser.add_argument("projetacoder", type=str, help="Objectif du projet à coder (obligatoire)")
parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds à exécuter (défaut : 5)")
parser.add_argument("--name", type=str, default=None, help="Nom du projet (facultatif, sinon généré)")
parser.add_argument("--review", type=int, default=3, help="Nombre de cycles codeur-reviewer (défaut : 3, 0 = désactivé)")
parser.add_argument("--test", action="store_true", help="Activer une étape de test automatique (désactivée par défaut)")
parser.add_argument("--narrateur", action="store_true", help="Inclure un agent narratif (NarrativeDesigner)")
parser.add_argument("--narrator", dest="narrateur", action="store_true", help="Alias de --narrateur")
parser.add_argument("--load", action="store_true", help="Reprendre un projet existant à partir de son nom")
parser.add_argument("--verbose", "-vv", action="store_true", help="Activer les logs détaillés")

args = parser.parse_args()

# === Chargement ou création ===
if args.load:
    if not args.name:
        raise ValueError("--load nécessite un --name pour identifier le projet existant.")
    print(f"🔄 Reprise du projet existant : {args.name}")
    team = CodeTeam.load_project(name=args.name, verbose=args.verbose)
else:
    print("=== Lancement d'un nouveau round de la CodeTeam ===")
    print(f"🎯 Objectif : {args.projetacoder}\n")
    print(f"📁 Projet : {args.name or '[généré]'} | Rounds : {args.n_round} | Review : {args.review} | Test : {args.test} | Narrateur : {args.narrateur}\n")

    team = CodeTeam(
        objectif=args.projetacoder,
        name=args.name,
        n_round=args.n_round,
        include_narrator=args.narrateur,
        max_review_cycles=args.review,
        enable_tests=args.test,
        verbose=args.verbose
    )

team.run()