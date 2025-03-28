# Projet MultiAgentIA

**Projet MultiAgentIA** est une plateforme modulaire visant à créer un système d'agents intelligents capables de collaborer de manière autonome ou en équipe.  
L'objectif ultime est de permettre à l'utilisateur de lancer des commandes en langage naturel (ex. : `code moi un jeu`) et d'obtenir des résultats cohérents issus de l'interaction de plusieurs agents spécialisés.

> **Objectif principal :**  
> Permettre aux utilisateurs de créer facilement des rôles, des agents et des teams pour répondre à des besoins spécifiques avec très peu de code, grâce à une architecture entièrement modulaire et extensible.

---

## Table des Matières

- [Aperçu](#aperçu)
- [Architecture](#architecture)
- [Fonctionnalités](#fonctionnalités)
- [Gestion des Bases de Données](#gestion-des-bases-de-données)
- [Utilisation](#utilisation)
- [Feuille de Route](#feuille-de-route)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Aperçu

**Projet MultiAgentIA** repose sur une architecture distribuée et modulaire. Chaque agent est composé de plusieurs composants clés :

- **Agents** : Dotés d’un rôle (contexte, objectifs, instructions spécifiques), d’une mémoire (court terme et long terme) et d’une compétence de raisonnement qui s’appuie sur un modèle de langage via un adaptateur LLM.
- **Communication** : Un système asynchrone gère l'échange d’objets `Message` entre agents. La communication peut fonctionner en mode autonome ou être centralisée via une team pour orchestrer les échanges.
- **Teams** : La classe `BaseTeam` (et ses sous-classes, ex. : `DebateTeam`) orchestre la discussion en diffusant un prompt initial et en gérant des cycles d'interaction.
- **Outils** : Des adaptateurs et autres outils (ex. : recherche web) enrichissent les capacités des agents.
- **Rôles** : Définis dans le dossier `roles`, ils apportent un contexte et des instructions qui influencent la génération des prompts par les agents.
- **Mémoire** : La gestion de la mémoire est assurée via deux modules distincts :
  - `short_term` contient la classe `ShortTermMemory` pour le suivi de l’historique conversationnel.
  - `long_term` contient la classe `LongTermMemory` pour une mémoire persistante.
- **Gestion des Bases de Données et Global Registry** :  
  - **db_management** : Module dédié à la gestion des bases de données utilisées pour la mémoire persistante des agents.
  - **global_registry** : Mécanisme d'adressage permettant de référencer et gérer plusieurs bases de données, facilitant leur création et leur utilisation.

> **Note :** Le dossier *envs* a été supprimé car il n'était pas utilisé actuellement.

---

## Architecture

L'architecture du projet est conçue pour offrir une **modularité** maximale et une **flexibilité d'utilisation** :

- **Modularité** :  
  Chaque composant (agent, rôle, skill, outil, team, module de DB) est développé indépendamment, permettant d'ajouter, de remplacer ou d'étendre des fonctionnalités sans réécrire l'ensemble du système.

- **Communication Asynchrone** :  
  Les agents échangent uniquement des objets `Message` enrichis de métadonnées. Le module de Communication, configurable via `config.py`, peut fonctionner en mode autonome ou être injecté par une team pour centraliser le routage des messages.

- **Flexibilité d'Usage** :  
  Les agents peuvent fonctionner seuls ou être regroupés en équipe. La classe `BaseTeam` orchestre les interactions collectives et peut être étendue pour répondre à des cas d’usage spécifiques.

- **Gestion des Bases de Données et Global Registry** :  
  La mémoire à long terme est gérée via une base de données, et le **global_registry** permet de gérer l'accès à ces bases sans modifier l'architecture globale, offrant ainsi la possibilité de créer ou d'utiliser différentes DB selon les besoins.

- **Configuration Globale** :  
  Le fichier `config.py` centralise des paramètres globaux, tels que :
  - `VERBOSE_COMMUNICATION` : Active ou désactive l'affichage des messages.
  - `DEFAULT_AFFICHAGE_FORCE` : Définit la valeur par défaut pour l'attribut `affichage_force` des messages.

- **Facilité de Création** :  
  Le système est conçu pour que l'utilisateur puisse créer de nouveaux rôles, agents et teams en écrivant très peu de code, facilitant ainsi la personnalisation et l'adaptation à des besoins spécifiques.

---

## Fonctionnalités

- **Agents Intelligents** :  
  - **Rôles** : Chaque agent reçoit un rôle qui fournit contexte, objectifs et instructions spécifiques.
  - **Raisonnement** : Les agents utilisent une compétence de reasoning s'appuyant sur un LLM via un adaptateur pour générer des réponses à partir de prompts enrichis (intégrant contexte, historique, etc.).
  - **Mémoire** : Gestion de la mémoire conversationnelle (ShortTermMemory) et possibilité d'une mémoire persistante (LongTermMemory).

- **Communication** :  
  - Échange asynchrone basé sur des objets `Message`.
  - Routage configurable des messages via des callbacks, permettant de gérer l'envoi vers un destinataire unique, un broadcast ou un message visible selon des flags (`dialogue`, `affichage_force`).

- **Teams Collaboratives** :  
  - La classe `BaseTeam` (et ses dérivées, ex. : `DebateTeam`) orchestre la discussion en envoyant un prompt initial et en gérant plusieurs tours d'interaction.
  - Possibilité de créer facilement des teams spécifiques pour des débats contradictoires ou d'autres cas d'usage.

- **Outils Intégrés** :  
  - Adaptateur LLM pour générer des réponses basées sur des prompts enrichis.
  - Possibilité d'intégrer d'autres outils (ex. : recherche web) pour étendre les capacités des agents.

- **Gestion des Bases de Données et Global Registry** :  
  - **db_management** : Module dédié à la gestion des bases de données utilisées pour la mémoire persistante des agents.
  - **global_registry** : Mécanisme central permettant de référencer et gérer plusieurs bases de données, facilitant leur création et leur utilisation dans divers contextes.

---

## Utilisation

### Pré-requis

- Python 3.x
- Installation des dépendances (voir `requirements.txt` s'il existe)

### Lancer un Débat

Pour lancer un débat contradictoire entre deux agents aux rôles opposés, exécutez :

```bash
git clone https://github.com/Tr1umV1RAT/Projet_MultiAgentIA.git
cd Projet_MultiAgentIA
python exemples/debate.py "le réchauffement climatique"
```
Sous Windows, dans le cas ou les packages du projet ne serait pas référencés, mettez vous simplement à la base du projet, ouvrez la console et entrez :

```bash
set PYTHONPATH=%cd%

```

Ce script instancie deux agents (par exemple, Alice avec un rôle scientifique et Bob avec un rôle climato-sceptique) et lance une discussion interactive sur le thème fourni.  
Les échanges se déroulent sur plusieurs tours (5 par défaut), et l'affichage des messages est contrôlé via le paramètre **VERBOSE_COMMUNICATION** défini dans `config.py` ou via les options de la team.

## Création Facile de Nouveaux Rôles, Agents et Teams

- **Rôles** :  
  Créez un nouveau rôle en étendant la classe `BaseRole` et en implémentant la méthode `generer_prompt()` (et éventuellement `get_extended_context()`).

- **Agents** :  
  Utilisez la classe `BaseAgent` en lui assignant un rôle.

- **Teams** :  
  Instanciez une équipe avec `BaseTeam` ou une sous-classe (ex. : `DebateTeam`), et fournissez une liste d'agents ainsi qu'un prompt initial optionnel.

## Feuille de Route

### Court Terme
- Finaliser et tester la communication asynchrone entre agents.
- Affiner l'intégration des rôles dans la génération de prompts, en incluant contexte étendu et historique.
- Valider les scénarios d'interaction pour des agents autonomes et en équipes via des tests d'intégration.

### Moyen Terme
- Intégrer de nouveaux outils (ex. : recherche web) pour enrichir les capacités des agents.
- Améliorer la gestion de la mémoire persistante (`LongTermMemory`) et intégrer le global registry pour la gestion des bases de données.

### Long Terme
- Étendre la modularité pour inclure de nouveaux types d'agents et de stratégies d'interaction (ex. : orchestration asynchrone avancée basée sur des événements).
- Renforcer la suite de tests unitaires et d'intégration pour garantir la robustesse globale du système.

## Contribuer

Les contributions sont les bienvenues !  
Pour contribuer, clonez le dépôt, créez une branche pour vos modifications, et soumettez une pull request :

```bash
git clone https://github.com/Tr1umV1RAT/Projet_MultiAgentIA.git
```

## Licence

Ce projet est sous licence **Apache 2.0**.
# Projet MultiAgentIA

Le **Projet MultiAgentIA** est une initiative open-source dont l'objectif est de fournir une plateforme flexible et modulaire pour créer, orchestrer et faire interagir facilement des agents intelligents pilotés par des modèles d'intelligence artificielle (LLM). La philosophie centrale du projet repose sur une modularité extrême et une simplicité d'utilisation permettant à tout utilisateur, même sans connaissance approfondie en IA, de composer et de contrôler des équipes d'agents pour diverses applications : développement logiciel, débats structurés, analyses, scénarisation de jeux, etc.

## Philosophie du Projet

- **Modularité** : Chaque composant (agents, rôles, skills, outils) est conçu pour être autonome, réutilisable, et interchangeable facilement.
- **Simplicité** : Des interfaces simples (CLI et API) permettent une prise en main rapide et une intégration aisée dans divers contextes d'utilisation.

## Structure du Projet

### Composants Principaux
- **Agents** : Entités intelligentes exécutant des tâches spécifiques grâce à des rôles et des compétences définies.
- **Rôles** : Définissent les objectifs et outils propres à chaque type d'agent.
- **Skills** : Capacités générales comme la mémoire ou le raisonnement, directement intégrées aux agents selon leur besoin.
- **Outils (Tools)** : Fonctions pratiques et réutilisables, telles que la recherche web ou la gestion de fichiers.
- **Équipes (Teams)** : Coordonnent les interactions et communications structurées entre plusieurs agents selon un scénario donné.

## Exemple d'utilisation

### Utiliser un agent directement depuis la ligne de commande
```bash
python agents/base_agent.py --name Agent1 --role Codeur --prompt "Écris une fonction Python qui trie une liste."
```

### Lancer une équipe complète (débat)
```bash
python exemples/debate_team.py --sujet "L'IA est-elle bénéfique pour l'humanité ?" --n_round 10
```

### Si vous êtes sous windows et que votre ordinateur ne reconnait pas les fichiers du projets comme des packages python, placez vous à la racine, ouvrez la console et tapez :

```bash
set PYTHONPATH=%cd%

```

## Axes d'Amélioration à Venir
- **Interface utilisateur avancée** : Développement d'une interface graphique intuitive pour gérer plus facilement les équipes et visualiser les interactions.
- **Optimisation mémoire** : Amélioration de la gestion dynamique de la mémoire (court et long terme) pour des performances accrues.
- **Amélioration de l'autonomie** : Capacités accrues des agents à sélectionner dynamiquement leurs propres outils et compétences selon la situation.
- **Documentation étendue** : Complétion et enrichissement de la documentation technique et des exemples d'usage.
- **Gestion avancée des projets** : Mise en place de mécanismes robustes de gestion des historiques et des versions de projets.

---

Le projet étant toujours en développement actif, vos contributions, suggestions et commentaires sont essentiels pour l'améliorer continuellement. N'hésitez pas à participer !

