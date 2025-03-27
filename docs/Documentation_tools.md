# 📚 Documentation Technique : Les Tools

---

## 🔧 BaseTool (`base_tool.py`)

**Classe abstraite** définissant la structure minimale pour tous les outils spécifiques du projet.

### 📥 Imports :
- `ABC` et `abstractmethod` du module `abc` :
  - Permettent de définir des classes abstraites en Python.

### 📌 Méthodes :
- `__init__(self, name: str, description: str = "")` :
  - Initialise l'outil avec un nom et une description optionnelle.
- `run(self, prompt: str) -> str` *(abstraite)* :
  - Méthode abstraite que chaque outil concret doit implémenter pour exécuter sa fonctionnalité.

---

## 📦 ArchivageTool (`archivage_tool.py`)

Permet aux agents d'archiver durablement des messages dans la mémoire à long terme.

### 📥 Imports :
- `Message` *(depuis `skills.communication.messages`)* : Structure standard des messages.
- `LongTermMemory` *(depuis `skills.memory.long_term`)* : Gestion de la mémoire à long terme.

### 📌 Méthodes :
- `__init__(self, agent, db_path="long_term_archive.db", verbose=False)` :
  - Initialise l'outil avec un agent associé, un chemin pour la base de données et une option de verbosité.
- `handle_message(self, message: Message, agent=None)` :
  - Archive le message reçu dans la mémoire à long terme.
  - Retourne un message de confirmation indiquant la réussite de l'opération.

---

## 🧠 LLMInterface (`llm_interface.py`)

Interface de communication simplifiée avec un modèle de langage local via Ollama.

### 📥 Imports :
- `requests` : Effectue des requêtes HTTP.
- `json` : Traitement des données au format JSON.
- `ollama` : Client Python (facultatif, mais importé explicitement dans le code original).

### 📌 Méthodes :
- `__init__(self, model="ollama", agent=None, verbose=False, host="localhost", port=11434)` :
  - Initialise l'interface avec le modèle spécifié, l'agent associé, l'adresse du serveur Ollama et le port.
- `query(self, prompt: str, context=None, options=None)` :
  - Sélectionne la méthode appropriée pour requêter le modèle.
- `query_ollama(self, prompt: str, context=None, options=None)` :
  - Envoie explicitement une requête HTTP à l'API Ollama et récupère la réponse du modèle.

---

## 📂 ProjectIO (`project_io.py`)

Gère explicitement toutes les opérations d'entrée-sortie relatives aux fichiers et dossiers du projet.

### 📥 Imports :
- `os` : Manipulations liées au système de fichiers.
- `json` : Sérialisation et désérialisation de données.
- `shutil` : Opérations avancées de gestion des fichiers.

### 📌 Méthodes statiques :
- `save_project(project_data, filepath)` : Enregistre les données du projet au format JSON.
- `load_project(filepath)` : Charge des données JSON depuis un fichier.
- `ensure_dir(directory)` : Crée un répertoire s’il n'existe pas.
- `delete_file(filepath)` : Supprime explicitement un fichier spécifié.
- `copy_file(src, dst)` : Copie explicitement un fichier d'une source à une destination.
- `move_file(src, dst)` : Déplace explicitement un fichier.
- `list_files(directory, extension=None)` : Liste les fichiers dans un répertoire, éventuellement filtrés par extension.

---

## 🛠️ SkillManagerTool (`skill_manager.py`)

Permet aux agents d'interagir explicitement avec leurs propres Skills internes.

### 📌 Méthodes :
- `__init__(self, agent)` :
  - Initialise avec une référence explicite à l'agent associé.
- `list_skills(self)` :
  - Retourne explicitement une liste des noms des Skills actuellement disponibles pour l'agent.
- `get_skill(self, skill_name: str)` :
  - Recherche explicitement et retourne un Skill spécifique par son nom.
- `execute_skill(self, skill_name: str, message)` :
  - Exécute explicitement un Skill spécifique en lui passant un message, renvoie une erreur si le Skill n'existe pas ou ne peut être exécuté.

---

## 🌐 WebSearchTool (`web_search.py`)

Réalise une recherche web simplifiée à l'aide d'un modèle de langage local (Ollama).

### 📥 Imports :
- `requests` : Effectue explicitement des requêtes HTTP.
- `BaseTool` *(depuis `tools.base_tool`)* : Héritage commun à tous les outils spécifiques.

### 📌 Méthodes :
- `__init__(self, name="WebSearch", model="mistral")` :
  - Initialise explicitement l'outil de recherche web avec un modèle spécifié.
- `run(self, query)` :
  - Requête explicitement Ollama avec un prompt demandant un résumé court sur la requête.
  - Retourne la réponse ou une erreur clairement détaillée si la requête échoue.

---

