import os
from datetime import datetime

class SkillNarrative:
    def __init__(self, agent, project_path="project_outputs", memory=None, verbose=False):
        self.agent = agent
        self.project_path = os.path.join(project_path, "narration")
        self.memory = memory
        self.verbose = verbose

        os.makedirs(self.project_path, exist_ok=True)

    def generate_narrative(self, objectif: str = None, code_en_cours: str = None, phase="initial") -> str:
        if phase == "initial":
            prompt = f"""
Tu es un Narrative Designer IA. Ta mission est de créer un scénario narratif immersif, utilisable dans un projet de développement logiciel (ex : jeu, simulateur, application interactive).

Objectif global du projet : {objectif}

Génère un contexte narratif cohérent : univers, ambiance, personnages principaux, quête centrale, antagonistes, tensions.
N'utilise aucun code. Structure le résultat par parties : Monde, Objectif du joueur, Ennemis, Événements, Style.
"""
        else:
            prompt = f"""
Tu es un Narrative Designer IA. Tu enrichis des projets logiciels par des éléments narratifs précis et ciblés.

Voici le code actuellement en cours d'écriture :
{code_en_cours}

Tu dois suggérer des ajouts narratifs exploitables par un Codeur :
- noms de variables, fonctions ou personnages
- dialogues à afficher
- objectifs de quête ou de mission

Formule tes suggestions de manière précise, sans jamais écrire de code.
Exemples :
- "Ajoute une ligne dans 'init_boss' affichant : 'Le chaos approche... Arkaal se réveille.'"
- "Renomme la variable 'enemy' en 'spectreDesRuines'."

Tu ne modifies jamais la structure technique du projet.
Tu ne proposes jamais de code brut. Tes suggestions doivent être ciblées, précises, et localisables.
"""

        suggestions = self.agent.llm.query(prompt)

        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"narration_{phase}_{timestamp}.md"
        filepath = os.path.join(self.project_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(suggestions)

        if self.verbose:
            print(f"[SkillNarrative] Narration sauvegardée dans : {filepath}")

        if self.memory:
            self.memory.store_document(
                content=suggestions,
                metadata={
                    "type": "narrative",
                    "phase": phase,
                    "objectif": objectif if objectif else "",
                    "timestamp": timestamp
                }
            )

        return suggestions