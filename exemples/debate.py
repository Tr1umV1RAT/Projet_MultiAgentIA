#!/usr/bin/env python
"""
debate.py
---------
Ce script lance un débat contradictoire entre deux agents ayant des rôles opposés.
Le prompt initial est passé en ligne de commande ou défini par défaut.
"""

import sys
from teams.debate_team import DebateTeam
from agents.base_agent import BaseAgent
from roles.base_role import BaseRole

# Définition d'un rôle scientifique
class RoleScientifique(BaseRole):
    def __init__(self):
        super().__init__(
            nom_role="Scientifique",
            objectif="Défendre le consensus scientifique sur le réchauffement climatique.",
            contexte="Tu es un scientifique engagé dans la défense des données établies.",
            instructions_specifiques="Utilise des preuves empiriques et des références scientifiques."
        )
    
    def get_extended_context(self) -> str:
        return "Ton expertise repose sur des études approfondies et des données fiables."

# Définition d'un rôle climato-sceptique
class RoleClimatoSceptique(BaseRole):
    def __init__(self):
        super().__init__(
            nom_role="ClimatoSceptique",
            objectif="Mettre en doute les modèles climatiques et proposer des interprétations alternatives.",
            contexte="Tu es sceptique face aux prévisions climatiques établies.",
            instructions_specifiques="Mets en avant l'incertitude et les limites des modèles."
        )
    
    def get_extended_context(self) -> str:
        return "Ta position se fonde sur une analyse critique des données et une attention aux incertitudes."

def main():
    # Récupérer le prompt initial depuis la ligne de commande, si fourni, sinon utiliser un prompt par défaut.
    if len(sys.argv) > 1:
        prompt_initial = sys.argv[1]
    else:
        prompt_initial = "Débattez du réchauffement climatique."
    
    # Création des agents avec leurs rôles respectifs
    agent_scientifique = BaseAgent("Alice", RoleScientifique())
    agent_sceptique = BaseAgent("Bob", RoleClimatoSceptique())
    
    # Création de la DebateTeam.
    # Les paramètres n_rounds, verbose et distribuer_prompt_initial utiliseront leurs valeurs par défaut (5, True, True).
    debat_team = DebateTeam(
        nom_team="DebatClimatique",
        prompt_initial=prompt_initial,
        agents=[agent_scientifique, agent_sceptique]
    )
    
    # Lancer le débat : envoi du prompt initial (si activé), puis traitement des messages sur plusieurs tours.
    debat_team.run()
    debat_team.cloturer()

if __name__ == '__main__':
    main()
