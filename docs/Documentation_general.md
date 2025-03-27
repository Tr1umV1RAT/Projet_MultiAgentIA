
# Documentation Technique Complète

## 1. Présentation de l'Architecture

Le projet est organisé selon une architecture modulaire orientée agents intelligents. L'architecture principale comprend les composants suivants :

- **Agents** : Instances intelligentes capables d'interagir entre elles et avec l'environnement.
- **Roles** : Définitions des contextes et objectifs spécifiques à chaque agent.
- **Skills** : Capacités génériques attribuées aux agents pour accomplir des tâches spécifiques.
- **Teams** : Organisation d'agents en équipes pour gérer des interactions structurées -> Voir documentation spécifique.
- **Tools** : Outils externes fournissant des fonctionnalités spécialisées aux agents.

## 2. Agents

### Classe `BaseAgent` (`agents/base_agent.py`)

Classe fondamentale pour tous les agents, définissant la gestion de la mémoire, communication et interactions via LLM.

#### Méthodes principales

- **`__init__(name, role, skills=None, verbose=False, communication=None, llm=None, memory_enabled=True)`** : Initialise l'agent avec un nom, un rôle, une liste optionnelle de skills, un système de communication, une instance LLM et une mémoire optionnelle.
- **`init_default_skills()`** : Initialise les skills par défaut (communication, retriever, gestion de la mémoire si activée).
- **`init_memory(base_path="agent_memories")`** : Initialise les différents types de mémoires (STM, LTM, WorkingMemory) en spécifiant un chemin pour la base de données.
- **`receive_message(message: Message)`** : Reçoit et stocke les messages entrants dans une file d'attente. Affiche le message reçu en mode verbeux.
- **`process_messages()`** : Traite chaque message reçu en générant une réponse appropriée via LLM, stocke les interactions dans la mémoire et les communique.
- **`get_prompt_context()`** : Retourne le prompt de rôle pour initialiser ou enrichir le contexte.
- **`objectif` (property)** : Retourne l'objectif spécifique de l'agent en récupérant l'attribut correspondant depuis son rôle.
- **`__repr__()`** : Retourne une représentation textuelle de l'agent incluant son nom et son rôle.

### Interface CLI (en fin de fichier base_agent.py)

Permet d'exécuter un agent directement depuis la ligne de commande :

```python
if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:])

    if not prompt:
        print("Veuillez fournir un prompt.")
        sys.exit(1)

    from roles.base_role import BaseRole
    role = BaseRole(name="DefaultAgent", objectif="Conversation générale")
    agent = BaseAgent(name="AgentCLI", role=role)

    message_recu = Message(contenu=prompt, origine="user", destinataire="AgentCLI")
    agent.receive_message(message_recu)
    agent.process_messages()
```

- L'utilisateur lance l'agent via la commande : `python base_agent.py "Votre message"`
- Le message fourni en argument est passé à l'agent qui le traite et répond.

### Exemple détaillé : AgentCodeur (`agents/agent_codeur.py`)

L'AgentCodeur hérite de BaseAgent et utilise spécifiquement un skill de post-processing du code généré.

#### Construction détaillée :

```python
from .base_agent import BaseAgent
from skills.coder.code_postprocessor_skill import CodePostprocessorSkill

class AgentCodeur(BaseAgent):
    def __init__(self, name, role, verbose=False, project_path="./temp_project"):
        super().__init__(name=name, role=role, verbose=verbose)
        self.project_path = project_path  # ✅ Gestion des fichiers projet

    def init_default_skills(self):
        skills = super().init_default_skills()
        skills.append(CodePostprocessorSkill(agent=self, project_path=self.project_path, verbose=self.verbose))
        return skills
```

- **`__init__`** : Initialise l'agent en spécifiant le chemin du projet utilisé pour le traitement post-génération de code. Cette initialisation appelle aussi celle du `BaseAgent`.
- **`init_default_skills`** : Ajoute spécifiquement le skill de post-processing (`CodePostprocessorSkill`) à l'agent après les skills par défaut.

Cet exemple montre comment spécialiser un agent en lui ajoutant des capacités additionnelles via des skills spécifiques tout en réutilisant les comportements définis dans `BaseAgent`.

## 3. Skills

### Base Skill (`skills/base_skill.py`)

Classe abstraite de base dont héritent tous les skills.

#### Méthodes principales

- **`__init__(agent=None, verbose=False)`** : 
  - **Variables** :
    - `agent`: Instance d'agent auquel appartient le skill.
    - `verbose`: Booléen activant les affichages détaillés.

- **`execute(*args, **kwargs)`** : 
  - **Variables** :
    - `*args`, `**kwargs`: Arguments variables permettant une flexibilité dans les implémentations.
  - Méthode abstraite qui doit être obligatoirement implémentée dans chaque sous-classe de skill pour exécuter la logique principale du skill.

### DBMixin (`skills/db_mixin.py`)

Mixin pour gérer la persistance dans une base de données SQLite.

#### Méthodes principales

- **`__getstate__()`** : 
  - Supprime les attributs non sérialisables (`connexion`, `cursor`) afin de permettre la sérialisation avec Pickle.

- **`__setstate__(state)`** : 
  - **Imports** : `import sqlite3`, `from config import MEMORY_TABLE_SCHEMA`
  - Rétablit l'état de l'objet en recréant la connexion et le curseur SQLite et en initialisant le schéma de la base de données spécifié par `MEMORY_TABLE_SCHEMA`.
  - **Variables** :
    - `self.db_name` : Nom de la base de données SQLite à connecter.
    - `self.connexion` : Objet de connexion SQLite.
    - `self.cursor` : Curseur SQLite utilisé pour exécuter les requêtes SQL.

### Reasoning Skill (`skills/reasoning.py`)

Capacité permettant à l'agent de générer un raisonnement structuré via LLM.

#### Méthodes principales

- **`__init__(agent, verbose=False)`** : 
  - Initialise le skill avec une référence vers l'agent possédant le skill (`agent`) et une option de verbosité (`verbose`).

- **`handle_message(message: Message, agent=None) -> Message`** : 
  - **Imports** :
    - `from skills.communication.messages import Message`
    - `from tools.llm_interface import LLMInterface`
  - **Variables** :
    - `message`: Instance de la classe Message reçue et à traiter.
    - `agent`: Agent traitant le message, par défaut celui du skill.
  - **Déroulement** :
    1. Vérifie la validité du message.
    2. Récupère le prompt spécifique au rôle de l'agent via `agent.role.get_prompt(message)`.
    3. Utilise l'outil LLM associé au rôle (`llm_tool`) récupéré par `_get_llm_tool_from_role(agent.role)` pour générer une réponse basée sur le prompt.
    4. Génère et retourne une nouvelle instance de Message avec la réponse obtenue du LLM.

- **`_get_llm_tool_from_role(role)`** : 
  - **Variables** :
    - `role`: Rôle de l'agent contenant potentiellement l'outil LLM.
  - Itère sur les outils (`role.outils`) associés au rôle pour identifier et retourner une instance d'`LLMInterface`. Retourne `None` si aucun outil LLM n'est trouvé.

### Communication Skill (`skills/communication/communication.py`)

Gère l'envoi et la réception de messages entre les agents.

#### Méthodes principales

- **`__init__(verbose=False)`** : 
  - Initialise le système de communication avec un mode verbeux optionnel pour afficher les messages de manière détaillée.

- **`send(message: Message)`** : 
  - **Imports** : `from .messages import Message`
  - **Variables** :
    - `message`: Instance de Message à envoyer.
  - Envoie un message vers les agents destinataires spécifiés dans l'attribut `message.destinataire`.

- **`receive()`** : 
  - Méthode prévue pour gérer la réception des messages entrants, actuellement définie pour extension future.

### Messages (`skills/communication/messages.py`)

Définit la structure et le comportement des messages échangés entre les agents.

#### Classe `Message`

- **`__init__(id, origine, destinataire, type_message="text", contenu="", importance=1, memoriser=True, dialogue=True, action="", affichage_force=False, version_finale=False, date=None, meta=None, conversation_id="")`** :
  - **Variables** :
    - `id`: Identifiant unique du message (généré automatiquement si non fourni).
    - `origine`: Expéditeur du message.
    - `destinataire`: Destinataire(s) du message.
    - `type_message`: Type du message (`"text"` par défaut).
    - `contenu`: Contenu textuel du message.
    - `importance`: Niveau d'importance du message.
    - `memoriser`: Indique si le message doit être mémorisé.
    - `dialogue`: Indique si le message fait partie d'un dialogue.
    - `action`: Action éventuelle associée au message.
    - `affichage_force`: Indique si l'affichage du message doit être forcé.
    - `version_finale`: Indique si c'est une version finale du message.
    - `date`: Date de création (automatiquement définie si non précisée).
    - `meta`: Métadonnées additionnelles.
    - `conversation_id`: Identifiant de la conversation associée.

- **`create(data)`** : 
  - Crée un message à partir d'une instance existante ou d'un dictionnaire contenant les attributs nécessaires.

- **`is_valid()`** : 
  - Vérifie la validité d'un message en s'assurant que les champs essentiels (`origine`, `destinataire`, `contenu`) sont présents.

- **`to_dict()` et `from_dict(data)`** : 
  - Sérialise et désérialise un message vers/depuis un dictionnaire pour faciliter son stockage ou sa transmission.

- **`to_json()`** : 
  - Sérialise le message en format JSON.

- **`__repr__()`** : 
  - Fournit une représentation textuelle concise du message, incluant son type, son origine et son destinataire.


### Mémoire (`skills/memory`)

#### BaseMemory (`skills/memory/base_memory.py`)

Classe abstraite définissant l'interface de base pour toutes les mémoires.

- **`__init__(agent, verbose=False)`** : Initialise avec une référence à l'agent possesseur et un mode verbeux.
- **`store(data)`** : Méthode abstraite pour stocker des données.
- **`retrieve(query)`** : Méthode abstraite pour récupérer des données selon une requête.

#### ShortTermMemory (`skills/memory/short_term_memory.py`)

Implémentation concrète de la mémoire à court terme (STM).

- **`__init__(agent, limit=100, verbose=False)`** : Initialise avec un agent, une limite de taille, et mode verbeux.
- **`store(data)`** : Stocke des données en mémoire temporaire jusqu'à atteindre la limite définie.
- **`retrieve()`** : Retourne les données actuelles en STM.

#### LongTermMemory (`skills/memory/long_term_memory.py`)

Implémentation concrète de la mémoire à long terme (LTM) avec SQLite.

- **`__init__(agent, db_path, verbose=False)`** : Initialise avec un agent et chemin vers la base de données.
- **`store(data)`** : Stocke durablement les données dans une base SQLite.
- **`retrieve(query)`** : Effectue une requête SQL pour récupérer les souvenirs pertinents.

#### WorkingMemory (`skills/memory/working_memory.py`)

Mémoire dynamique générée à partir de la mémoire long terme et du contexte actuel via LLM.

- **`__init__(agent, verbose=False)`** : Initialise avec une référence à l'agent.
- **`generate(context)`** : Génère un résumé dynamique des informations pertinentes à partir du contexte.

#### MemoryManager (`skills/memory/memory_manager.py`)

Gère la coordination entre STM, LTM, et WorkingMemory.

- **`__init__(agent, verbose=False)`** : Initialise en coordonnant toutes les mémoires de l'agent.
- **`store_message(message)`** : Stocke un message simultanément dans les mémoires appropriées.
- **`retrieve_context(query)`** : Génère un contexte utile combinant STM, LTM et WorkingMemory pour répondre efficacement à une requête.

#### MemoryRetriever (`skills/memory/memory_retriever.py`)

Skill spécifique facilitant la récupération intelligente des informations depuis la mémoire.

- **`__init__(agent, verbose=False)`** : Initialise avec l'agent référent.
- **`build_context(message)`** : Crée un contexte enrichi en utilisant la mémoire pour améliorer les réponses aux messages.

#### MemoryInspector (`skills/memory/memory_inspector.py`)

Permet l'inspection des contenus des différentes mémoires.

- **`inspect_memory(memory)`** : Affiche clairement le contenu d'une mémoire spécifiée pour diagnostic ou débogage.

#### MemoryInspectorSkill (`skills/memory/memory_inspector_skill.py`)

Skill permettant l'utilisation simplifiée du MemoryInspector par les agents.

- **`__init__(agent, verbose=False)`** : Initialise avec référence à l'agent.
- **`execute(memory_type)`** : Facilite l'inspection directe d'un type de mémoire spécifié.

#### MemoryAccess (`skills/memory/memory_access.py`)

Gère les autorisations et les logs d'accès sécurisés à la mémoire entre agents.

- **`__init__(agent, memory_owner, verbose=False)`** : Initialise avec l'agent demandeur et l'agent propriétaire de la mémoire.
- **`is_authorized(reason)`** : Vérifie les autorisations d'accès selon la raison spécifiée.
- **`log_access(action, meta)`** : Enregistre un log détaillé des accès à la mémoire.
- **`read(long_term_memory, filtre)`** : Lit de manière sécurisée des données spécifiques en mémoire.

### Fonctionnement technique complet de la mémoire

Le système de mémoire est structuré en trois niveaux distincts :

- **Mémoire à Court Terme (STM)** : Stocke temporairement les messages et informations récentes pour un accès rapide durant les interactions immédiates. Elle est volatile et limitée en capacité.

- **Mémoire à Long Terme (LTM)** : Utilise SQLite pour persister durablement les informations importantes sur le long terme. Elle permet aux agents de récupérer des souvenirs pertinents à travers des requêtes précises.

- **Mémoire de Travail (WorkingMemory)** : Génère dynamiquement un contexte résumé en combinant intelligemment les données issues de la LTM et du contexte immédiat via un modèle de langage (LLM).

Le `MemoryManager` orchestre ces différentes mémoires, assurant une cohérence et une efficacité optimale dans la gestion des informations. Le `MemoryRetriever` améliore les réponses des agents en construisant un contexte pertinent à partir des mémoires disponibles.

Le système intègre aussi des outils d'inspection (`MemoryInspector`) et de gestion des accès sécurisés (`MemoryAccess`), permettant une gestion fine et sécurisée de l'information au sein du projet.

## 4. Skills spécialisés 


### Coder

#### CodePostProcessorSkill (`skills/coder/code_postprocessor_skill.py`)

- **Imports** :
  - `os` : Module pour la gestion du système de fichiers.
  - `re` : Expressions régulières pour l'extraction du code.
  - `uuid` : Génération d'identifiants uniques pour les noms de fichiers.
  - `Optional` depuis `typing` : Typage optionnel pour certaines fonctions.
  - `BaseSkill` depuis `skills.base_skill` : Classe de base dont hérite ce skill.
  - `Message` depuis `skills.communication.messages` : Classe définissant la structure des messages échangés.
  - `MemoryManagerTool` depuis `skills.memory.memory_manager` : Outil pour la gestion de la mémoire.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise le skill avec une référence à l'agent (`agent`) auquel le skill appartient, ainsi qu'une option de verbosité (`verbose`) pour l'affichage détaillé des opérations.

  - **`handle_message(self, message: Message, agent=None) -> Message`** :
    - Reçoit et traite un message entrant (`message`).
    - **Étapes détaillées** :
      1. Vérifie la validité du message reçu.
      2. Extrait le code du contenu du message via `_extract_code()`.
      3. Extrait le nom du fichier cible via `_extract_filename()`. Si aucun nom n'est trouvé, génère automatiquement un nom via `_generate_filename()`.
      4. Sauvegarde le code extrait dans un fichier au chemin déterminé par `agent.project_path` via `_save_code_to_file()`.
      5. Recherche un skill de gestion de base de données via `_get_db_skill()` pour enregistrer l'opération effectuée.
      6. Retourne un nouveau `Message` confirmant l'extraction et la sauvegarde du code.

  - **`_extract_code(self, text: str) -> str`** :
    - Extrait le code Python du texte (`text`) en utilisant une expression régulière.

  - **`_extract_filename(self, text: str) -> Optional[str]`** :
    - Extrait le nom du fichier spécifié dans le texte (`text`) via une expression régulière. Retourne `None` si aucun nom n'est trouvé.

  - **`_generate_filename(self) -> str`** :
    - Génère automatiquement un nom de fichier unique au format UUID raccourci, suivi de l'extension `.py`.

  - **`_save_code_to_file(self, path: str, code: str)`** :
    - Crée le dossier parent si nécessaire, puis écrit le code (`code`) dans un fichier spécifié par le chemin (`path`).

  - **`_get_db_skill(self)`** :
    - Recherche parmi les skills de l'agent un skill capable de sauvegarder des messages en base de données. Retourne ce skill ou `None` si aucun n'est trouvé.




#### CoderSkill (`skills/coder/coder_skill.py`)

- **Imports** :
  - `LLMInterface` depuis `tools.llm_interface` : Interface pour interagir avec le modèle de langage.
  - `BaseSkill` depuis `skills.base_skill` : Classe de base des skills.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise avec une référence à l'agent (`agent`) possédant le skill et une option verbosité (`verbose`).

  - **`generate_code(self, prompt)`** :
    - Génère du code à partir du prompt (`prompt`) fourni.
    - Utilise l'interface LLM (`LLMInterface`) associée à l'agent pour interagir avec le modèle de langage et retourner le code généré.

### DB Management

#### DBManagement (`skills/db_management/db_management.py`)

- **Imports** :
  - `sqlite3` : Gestion de bases de données SQLite.
  - `BaseSkill` depuis `skills.base_skill` : Héritage des méthodes communes aux skills.

- **Méthodes détaillées** :
  - **`__init__(self, agent, db_path, verbose=False)`** :
    - Établit une connexion à une base SQLite définie par le chemin (`db_path`) et initialise l'agent et le mode verbeux.

  - **`store_data(self, table, data)`** :
    - Insère les données spécifiées (`data`) dans la table spécifiée (`table`).

  - **`retrieve_data(self, table, condition)`** :
    - Exécute une requête SQL avec une condition (`condition`) afin de récupérer des données précises dans la table (`table`).

#### GlobalRegistry (`skills/db_management/global_registry.py`)

- **Imports** :
  - `sqlite3` : Gestion de bases de données SQLite.

- **Méthodes détaillées** :
  - **`__init__(self, db_path, verbose=False)`** :
    - Initialise le registre global à partir d'une base SQLite (`db_path`) avec une option de verbosité.

  - **`register(self, key, value)`** :
    - Enregistre une nouvelle entrée dans le registre global associant une clé (`key`) à une valeur (`value`).

  - **`retrieve(self, key)`** :
    - Récupère la valeur associée à une clé (`key`) spécifiée.

### Planning

#### PlanExecutor (`skills/planning/plan_executor.py`)

- **Imports** :
  - `BaseSkill` depuis `skills.base_skill` : Héritage pour définir le comportement commun.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise l'exécuteur avec référence à l'agent et option verbosité.

  - **`execute_plan(self, plan)`** :
    - Exécute chaque étape spécifiée dans le plan (`plan`) donné, coordonnant l'action via les capacités disponibles de l'agent.

#### PlanificationSkill (`skills/planning/planification_skill.py`)

- **Imports** :
  - `LLMInterface` depuis `tools.llm_interface` : Interaction avec le modèle de langage.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise la capacité de planification avec une référence à l'agent et verbosité.

  - **`generate_plan(self, objective)`** :
    - Génère un plan structuré répondant précisément à l'objectif (`objective`) spécifié en utilisant l'interface LLM.

#### SkillPlanner (`skills/planning/skill_planner.py`)

- **Imports** :
  - `BaseSkill` depuis `skills.base_skill` : Héritage des méthodes communes.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise avec référence à l'agent et option verbosité.

  - **`plan_skills(self, task)`** :
    - Détermine l'ordre optimal d'utilisation des skills disponibles pour réaliser efficacement une tâche (`task`).

### Reviewer

#### ReviewSkill (`skills/reviewer/review_skill.py`)

- **Imports** :
  - `LLMInterface` depuis `tools.llm_interface` : Pour interaction avec le modèle de langage.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise la capacité de revue critique associée à l'agent spécifié.

  - **`review_content(self, content)`** :
    - Génère une revue critique détaillée du contenu fourni (`content`) via l'interaction avec LLMInterface.

### Synthétiseur

#### SyntheseSkill (`skills/synthetiseur/synthese_skill.py`)

- **Imports** :
  - `LLMInterface` depuis `tools.llm_interface` : Pour interaction avec le modèle de langage.

- **Méthodes détaillées** :
  - **`__init__(self, agent, verbose=False)`** :
    - Initialise la capacité de synthèse d'informations associée à l'agent spécifié.

  - **`generate_summary(self, contents)`** :
    - Génère un résumé clair, précis et synthétique à partir des contenus fournis (`contents`) via LLMInterface.


## 5. Rôles


### BaseRole (`roles/base_role.py`)

- **Classe fondamentale définissant la structure minimale des rôles utilisés par les agents.**

- **Imports :** Aucun import externe requis.

- **Méthodes détaillées :**
  
  - **`__init__(self, name: str, objectif: str, contexte: str = "", instructions_specifiques: str = "", outils: list = None)`** :
    - Initialise les attributs fondamentaux du rôle.
    - **Variables :**
      - `name` (str) : Nom explicite du rôle.
      - `objectif` (str) : Objectif principal clairement défini du rôle.
      - `contexte` (str, optionnel) : Contexte spécifique dans lequel s'inscrit le rôle.
      - `instructions_specifiques` (str, optionnel) : Directives supplémentaires spécifiques au rôle.
      - `outils` (list, optionnel) : Liste des outils spécifiques associés au rôle.

  - **`get_prompt(self, message: str) -> str`** :
    - Génère un prompt contextuel enrichi de tous les éléments définis dans le rôle et du message reçu.
    - **Paramètres :**
      - `message` (str) : Message ou tâche à traiter.
    - **Retour :** Prompt complet formaté pour être envoyé au modèle de langage (LLM).

  - **`get_outils(self)`** :
    - Retourne la liste des outils associés à ce rôle.

  - **`__repr__(self)`** :
    - Retourne une représentation lisible du rôle indiquant son nom.

### Exemple détaillé : CodeurRole (`roles/codeur.py`)

- **Classe spécifique définissant un rôle dédié à la génération de code clair et fonctionnel.**

- **Imports :**
  - `BaseRole` depuis `roles.base_role` : Hérite des attributs et méthodes de base.

- **Méthodes détaillées :**
  
  - **`__init__(self)`** :
    - Initialise le rôle spécifique de codeur en appelant le constructeur de la classe parente (`BaseRole`).
    - **Variables héritées définies explicitement :**
      - `name` : Nom du rôle, ici "Codeur".
      - `objectif` : Objectif principal clairement formulé : écrire du code propre et conforme aux spécifications du projet.

  - **`get_prompt(self)`** :
    - Génère un prompt extrêmement détaillé et rigoureux, définissant précisément le contexte et les règles de génération de code.
    - **Directives spécifiques intégrées dans le prompt :**
      1. Encapsulation stricte des sorties de code dans des blocs Markdown Python clairement définis.
      2. Obligation d'utiliser des docstrings détaillées pour chaque fonction, précisant rôle, paramètres et retour.
      3. Interdiction explicite des noms de variables imprécis tels que `foo`, `x` ou `tmp`.
      4. Exigence de ne pas produire de texte inutile en dehors des blocs de code.
      5. Priorité absolue à la clarté, la modularité et l'adaptabilité du code généré.



