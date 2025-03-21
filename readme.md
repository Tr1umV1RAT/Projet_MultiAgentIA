# Projet MultiAgentIA

Ce projet vise à créer un système d'agents intelligents, modulaires et collaboratifs, capables de travailler seuls ou en équipe. Le but final est de permettre à un utilisateur de lancer des commandes (par exemple, "code moi un jeu") et d'obtenir un résultat cohérent et de haute qualité, généré par la collaboration de plusieurs agents spécialisés.

---

## 1. Concepts Clés

- **Modularité**  
  Le système est conçu pour être extrêmement modulaire :  
  - Chaque composant (agent, rôle, skill, outil, communication, mémoire) est développé de manière isolée pour faciliter l'extension et la maintenance.
  - Les rôles fournissent du contexte et des instructions spécifiques, influençant la génération des prompts pour l’IA.
  - L'utilisation des outils (comme les appels LLM et la recherche Web) est intégrée pour augmenter les capacités de chaque agent.

- **Mémoire**  
  - **Mémoire individuelle** : Chaque agent dispose d'une mémoire distincte, à court terme (en mémoire interne) et d'une mémoire persistante (base de données personnelle) qui peut être gérée indépendamment.
  - **Registre de bases de données** : Un registre global de DB est prévu pour éviter de réécrire toute la structure et permettre à un agent ou un module de créer et utiliser une base de données pour un usage spécifique.

- **Communication Inter-Agent**  
  - Les échanges se font via un système de messages enrichis (incluant des métadonnées).
  - Le système vise à rendre la communication entre agents aussi naturelle que possible dès l'utilisation d'une team. Un appel du type `BaseTeam(agent1, agent2, "prompt utilisateur")` devrait déclencher une interaction fluide.
  - La communication intègre les contextes fournis par les rôles, garantissant que l’IA génère des réponses alignées avec le profil de l’agent.

- **Utilisation des Outils**  
  - Chaque agent peut disposer d’outils spécifiques (ex. LLM, WebSearchTool) qui peuvent être invoqués directement ou via son rôle.
  - L'architecture permet une injection dynamique des outils selon le contexte ou le rôle assigné.

---

## 2. Architecture Technique

### Structure du Dépôt

- **agents/**  
  Contient la logique de base des agents, qui héritent d'une classe de base commune.
  
- **roles/**  
  Définit les rôles spécifiques (Scientifique, ClimatoSceptique, Codeur, Reviewer, etc.) qui apportent le contexte et les instructions propres à chaque agent.

- **skills/**  
  Modules de compétences (communication, reasoning, mémoire, etc.) permettant aux agents de traiter les messages et d'interagir avec le LLM.

- **tools/**  
  Contient les adaptateurs d'outils externes (ex. `llm_adapter.py`, `web_search_tool.py`). Le module `llm_adapter.py` centralise tous les appels LLM et lit les paramètres de configuration via `config.py`.

- **teams/**  
  Gère la composition des équipes d'agents et leur orchestration (ex. `DebateTeam`, `CodeTeam`).

- **utils/**  
  Contient les outils utilitaires divers.

- **config.py**  
  Fichier central de configuration où sont définis tous les paramètres clés : fournisseur LLM, modèle, endpoint, API key, mode d’injection, etc.

### Communication et Mémoire

- **Communication**  
  - La classe `Communication` gère l’envoi et la réception de messages entre agents.  
  - Le message contient des métadonnées (origine, destinataire, type, etc.) qui permettront d'acheminer les échanges de façon naturelle.

- **Mémoire**  
  - Chaque agent possède une mémoire courte (session interne) et une mémoire persistante (stockée dans une DB dédiée).
  - Le registre de DB est présent pour permettre à tout agent de créer ou utiliser une nouvelle base sans modifier la structure globale.

---

## 3. Feuille de Route

### A. Améliorations de la Communication Inter-Agent

- **Objectif** : Rendre les échanges plus naturels et interactifs.
  - Revoir la logique dans `BaseTeam` et/ou le module `Communication` pour que l'appel d'une team du type `BaseTeam(agent1, agent2, "prompt utilisateur")` déclenche une interaction réelle :
    - Diffuser la consigne à tous les agents impliqués.
    - Intégrer un mécanisme de boucle ou de médiation permettant à chaque agent de réagir aux réponses précédentes.
    - Revoir la gestion du champ `destinataire` pour que les messages ne soient pas seulement adressés au "System" mais redistribués aux agents concernés.
    
### B. Gestion de la Mémoire

- **Objectif** : Assurer que chaque agent dispose d'une mémoire distincte et exploitable, tout en permettant l'utilisation d'autres DB via le registre.
  - Implémenter l'usage actif de la mémoire dans les prompts en intégrant un résumé du contexte ou des messages précédents lors de l'appel au LLM (par exemple dans le module de reasoning ou directement dans `BaseRole.generer_prompt`).
  - Clarifier et unifier l'usage de la mémoire persistante et du registre de DB pour éviter les redondances (fusionner ou clarifier les rôles de `DBManagementSkill` et `LongTermMemory`).

### C. Amélioration de la Gestion des Outils

- **Objectif** : Faciliter l'injection et l'utilisation dynamique des outils.
  - Permettre, via la configuration (et/ou les rôles), l'ajout ou la suppression d'outils spécifiques sans modification directe du code.
  - Intégrer dans les prompts des indications sur l'utilisation possible des outils (ex. « Tu as accès à WebSearchTool. ») pour guider le LLM.
  - S'assurer que les appels aux outils génèrent bien une chaîne d'action (exécuter la commande et réinjecter le résultat dans la conversation).

### D. Modularité et Extension

- **Objectif** : Garder le principe de modularité comme maître-mot.
  - Vérifier que chaque composant (agent, rôle, skill, outil, équipe, mémoire) est bien découplé des autres et peut être remplacé ou étendu indépendamment.
  - Prévoir un mécanisme de "plug-in" pour faciliter l’ajout de nouveaux outils ou de nouvelles logiques de communication sans modifier le cœur du système.
  - Documenter les interfaces de chaque module pour que les futurs contributeurs (ou toi-même) puissent intervenir facilement sur chacun des composants.

---

## 4. Conclusion

Ce projet repose sur une architecture ambitieuse où la modularité est au cœur de la conception. Les axes d'amélioration principaux concernent :

- **La communication** : Rendre l'échange entre agents plus fluide et interactif.
- **La mémoire** : Utiliser activement la mémoire pour alimenter le contexte des débats et permettre aux agents d'avoir un historique dynamique.
- **Les outils** : Assurer une injection et une utilisation flexible des outils, sans modification directe du code.
- **La modularité** : Veiller à ce que chaque composant reste indépendant et facilement extensible.

Ce README se veut la base de discussion et d'évolution pour le projet. Chaque point de la feuille de route pourra être abordé et implémenté progressivement. L'idée est de construire un système d'agents collaboratifs qui reste fidèle à l'esprit de modularité et qui permette d'étendre, sans réécrire l'architecture, l'ensemble des fonctionnalités souhaitées.

---

## 5. Prochaines Étapes

1. **Communication**  
   - Revoir et modifier le module `Communication` et/ou `BaseTeam` pour gérer les échanges inter-agents de manière dynamique (envoi aux destinataires appropriés, gestion de tours de parole, etc.).

2. **Mémoire**  
   - Activer et exploiter la mémoire (tant courte que persistante) dans la génération des prompts via le module de reasoning.
   - Intégrer le registre de DB de façon cohérente dans le workflow.

3. **Outils**  
   - Ajouter des indications dans les rôles pour que le LLM sache exploiter les outils disponibles.
   - Vérifier que chaque outil est correctement injecté dans l'agent via son rôle.

4. **Documentation et Tests**  
   - Documenter en détail chaque module et prévoir des tests unitaires pour chaque composant afin d'assurer la robustesse du système.

Chaque étape devra être discutée et validée point par point pour s'assurer que le projet évolue dans la direction souhaitée.

---

*N'hésite pas à revenir vers moi pour approfondir chaque point ou pour toute autre question, Quentin !*
