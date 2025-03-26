# Projet MultiAgentIA – Documentation de l’Architecture

## Introduction

**Projet MultiAgentIA** est une plateforme modulaire visant à créer un système d’agents intelligents capables de collaborer de manière autonome ou en équipe. L’objectif est de permettre à un utilisateur, même non codeur, de lancer des commandes en langage naturel (par exemple, `python code_team.py "code moi un jeu"`) et d’obtenir un résultat cohérent issu de l’interaction de plusieurs agents spécialisés.

---

## Table des Matières

- [Objectifs et Philosophie](#objectifs-et-philosophie)
- [Architecture Générale](#architecture-générale)
  - [Agents](#agents)
  - [Rôles](#rôles)
  - [Skills](#skills)
  - [Tools](#tools)
  - [Communication](#communication)
  - [Mémoire](#mémoire)
  - [Teams](#teams)
- [Flux de Communication](#flux-de-communication)
- [Comparaison Agents Modernisés vs Agents Type 2](#comparaison-agents-modernisés-vs-agents-type-2)
- [Configuration et Environnement](#configuration-et-environnement)
- [Pistes d’Amélioration et Points de Vigilance](#pistes-damélioration-et-points-de-vigilance)
- [Erreurs et Incohérences Détectées](#erreurs-et-incohérences-détectées)
- [Conclusion](#conclusion)

---

## Objectifs et Philosophie

- **Modularité et Extensibilité :** Permettre la création et l’extension aisée des rôles, agents, teams et skills.
- **Interaction en Langage Naturel :** Unifier toutes les interactions via un système de messages.
- **Architecture Distribuée :** Chaque agent possède un rôle, une mémoire (court et long terme) et des compétences encapsulées dans des skills.
- **Facilité d’Utilisation :** À terme, un utilisateur non codeur pourra lancer le système via une commande simple.

---

## Architecture Générale

### Agents

- **Rôle :** Les agents sont les entités actives qui traitent les commandes, interagissent entre eux et exécutent des tâches spécifiques.
- **Structure :**
  - Héritent d’un **BaseAgent** qui centralise les fonctionnalités communes.
  - Les fonctionnalités spécifiques sont injectées via la méthode `init_default_skills()`.
- **Exemples :**
  - `AgentCodeur` (version modernisée) vs. `AgentCodeur2` (ancienne itération).
  - De même pour `AgentReviewer` et d’autres agents.

### Rôles

- **Fonction :** Les rôles fournissent le contexte, les instructions et les contraintes pour la génération des prompts et le comportement des agents.
- **Organisation :** Chaque agent se voit attribuer un rôle (ex. : `CodeurRole`, `ReviewerRole`, etc.), défini dans le dossier `roles/`.
- **Conditions :** Respecter la hiérarchie et les interfaces définies par la classe `base_role`.

### Skills

- **Définition :** Les skills sont des modules indépendants qui étendent les capacités des agents (ex. communication, gestion de bases de données, post-traitement de code, etc.).
- **Organisation :**
  - Se retrouvent dans le dossier `skills/`, avec des sous-dossiers dédiés (par exemple, `coder`, `communication`, `db_management`).
  - Doivent être compatibles avec la logique de `BaseAgent` et être injectés via la méthode `init_default_skills()`.

### Tools

- **Concept :** Les outils (via une éventuelle classe de base comme `base_tool`, à définir ou étendre) permettent d’intégrer des fonctionnalités externes (par exemple, recherche web, adaptateurs externes).
- **Intégration :** Leur utilisation se fait via la classe **Message** qui standardise l’échange de données entre agents et outils.

### Communication

- **Système Centralisé :** Toute la communication passe par des objets **Message**.
  - Cela inclut les interactions entre agents ou entre agents et outils.
- **Routage :** La classe `BaseTeam` gère le routage des messages via la méthode `_route_message`.
  - **Point d’attention :** Dans `BaseTeam`, la méthode `_route_message` semble incomplète (ligne tronquée : `if isinstance(d, str) and d i…`). Il faudra revoir et compléter cette partie pour assurer un routage correct.

### Mémoire

- **Deux Niveaux :**
  - **Mémoire Court Terme (ShortTermMemory) :** Conserve le contexte immédiat des interactions.
  - **Mémoire Long Terme (LongTermMemory) :** Stocke l’historique de façon persistante.
- **Objectif Futur :** Implémenter une « mémoire de travail » qui extrait les éléments pertinents du long terme pour enrichir le contexte à chaque interaction.
- **État Actuel :** Ces modules sont encore en phase d’ébauche et nécessitent une réflexion approfondie sur la logique de mise à jour et de filtrage.

### Teams

- **Rôle :** Les teams orchestrent les interactions entre agents et centralisent la communication.
- **Exemples :**
  - `BaseTeam` : classe de base pour les équipes.
  - `CodeTeam` : définit une équipe d’agents spécialisés (manager, codeur, reviewer, designer, narrateur, synthetiseur).
- **Fonctionnalités :**
  - Injection d’une instance commune de **Communication** dans chaque agent.
  - Distribution des messages selon des stratégies de routage.
  - Permet d’ajouter facilement des outils ou des skills au niveau de l’équipe.

---

## Flux de Communication

1. **Création du Message :**  
   Un agent ou un outil crée un objet **Message** incluant le contenu, le destinataire (ou la liste de destinataires) et des métadonnées.
2. **Envoi :**  
   Le message est envoyé via la méthode de communication associée.
3. **Routage :**  
   Le système de team, via la méthode `_route_message` de `BaseTeam`, distribue le message aux agents concernés.
4. **Réception et Traitement :**  
   Chaque agent reçoit et traite le message grâce à ses skills, qui peuvent inclure des opérations de post-traitement ou d’analyse (par exemple, pour la revue de code).

---

## Comparaison Agents Modernisés vs Agents Type 2

- **Agents Modernisés (sans suffixe "2") :**
  - Utilisent un **BaseAgent** épuré et injectent leurs fonctionnalités via des skills (méthode `init_default_skills()`).
  - Offrent une meilleure modularité, facilitant la maintenance et l’extension du système.
- **Agents Type 2 (suffixe "2") :**
  - Intègrent directement des modules de mémoire, de communication et de gestion de bases de données dans leur constructeur.
  - Sont plus verbeux et moins modulaires, ce qui complique la maintenance.
- **Recommandation :**  
  Poursuivre avec les agents modernisés et archiver ou supprimer les versions de type 2 pour éviter toute confusion.

---

## Configuration et Environnement

- **Fichier `config.py` :**  
  - Destiné à centraliser la configuration du projet (schéma de base de données, paramètres divers).
  - **Point à améliorer :** Le fichier est actuellement peu utilisé et devra être étendu pour supporter la configuration dynamique de l’ensemble des modules.
  
- **Fichier `requirements.txt` :**  
  - Liste des dépendances.
  - **Remarque :** Il semble généré à partir de ton environnement conda sous Windows. Il serait pertinent de le réviser pour n’inclure que les bibliothèques réellement utilisées.

---

## Pistes d’Amélioration et Points de Vigilance

1. **Documentation Complète :**  
   - Détail des rôles et responsabilités de chaque module (agents, roles, skills, tools, teams).
   - Explication du flux de communication via la classe **Message** et ses métadonnées.
2. **Tests et Validation :**  
   - Mise en place d'une suite de tests unitaires et d’intégration pour vérifier la cohérence des interactions entre agents.
   - Tests spécifiques pour le mécanisme de routage dans `BaseTeam`.
3. **Système de Mémoire :**  
   - Finaliser le design et l’implémentation du système de mémoire (court terme vs long terme).
   - Envisager de développer un **MemorySkill** dédié.
4. **Simplification de l’Architecture :**  
   - Archiver ou supprimer les anciens fichiers de type "2" pour clarifier la maintenance.
5. **Interface Utilisateur :**  
   - Prévoir l’ajout d’un système de gestion des arguments en ligne de commande pour lancer facilement une équipe d’agents (ex. : `python code_team.py "code moi un jeu"`).

---

## Erreurs et Incohérences Détectées

- **Méthode `_route_message` dans `BaseTeam` :**  
  - La méthode semble incomplète ou tronquée (ligne indiquant `if isinstance(d, str) and d i…`).  
  - **Action recommandée :** Vérifier et compléter cette partie pour assurer un routage correct des messages.
- **Agents Type 2 :**  
  - Les fichiers comme `agent_codeur2.py` et `agent_reviewer2.py` représentent d’anciennes itérations.  
  - **Action recommandée :** Archiver ces fichiers pour éviter toute confusion.
- **Fichier `requirements.txt` :**  
  - Doit être réécrit pour refléter les dépendances réelles du projet.

---

## Conclusion

Cette documentation constitue une base solide pour comprendre et développer le projet MultiAgentIA. Elle permet de :

- Mettre en lumière les composants clés et leurs interactions.
- Identifier les points d’amélioration, tant au niveau du code (notamment le mécanisme de routage) que de l’architecture (système de mémoire, gestion des agents).
- Guider les futures évolutions et extensions de la plateforme.

La documentation évoluera avec le projet. N’hésite pas à la compléter au fur et à mesure des avancées ou des nouvelles idées.

---


