# Documentation Technique : Classe `BaseTeam`

**Fichier** : `base_team.py`

## Présentation générale

La classe `BaseTeam` constitue l'élément central d'organisation des interactions entre plusieurs agents intelligents. Elle coordonne précisément les échanges de messages et gère l'orchestration des conversations structurées entre les agents qui lui sont rattachés.

---

## 📥 Imports détaillés

- **`argparse`** :
  - Permet une gestion avancée des arguments passés via la ligne de commande.

- **`Message`** *(depuis `skills.communication.messages`)* :
  - Structure fondamentale encapsulant les échanges d'informations entre les agents.

- **`Communication`** *(depuis `skills.communication.communication`)* :
  - Classe centrale assurant la gestion coordonnée de l'envoi et la réception de messages.

- **`BaseAgent`** *(depuis `agents.base_agent`)* :
  - Structure minimale commune à tous les agents participant aux interactions de la team.

- **`BaseRole`** *(depuis `roles.base_role`)* :
  - Fournit un contexte de base permettant aux agents dynamiques d’interagir immédiatement.

---

## 📌 Méthodes détaillées

### Constructeur : `__init__(self, nom_team, agents, n_rounds=5, prompt_initial=None, verbose=False)`

- **Paramètres :**
  - `nom_team` *(str)* : Nom unique de l'équipe créée.
  - `agents` *(list ou dict)* : Agents participant aux interactions.
  - `n_rounds` *(int, défaut=5)* : Nombre de cycles d'interaction.
  - `prompt_initial` *(str, optionnel)* : Message initial pour démarrer les interactions.
  - `verbose` *(bool, optionnel)* : Active l'affichage détaillé des opérations.

- **Actions réalisées :**
  - Convertit explicitement les agents en un dictionnaire interne (`agents_dict`).
  - Initialise une instance unique de `Communication`.
  - Injecte la communication commune à chaque agent avec la callback de routage.
  - Affiche l'état initial de la team en mode verbeux.

---

### Méthode : `route_message(self, message: Message)`

- **Paramètres :**
  - `message` *(Message)* : Message à router aux destinataires.

- **Fonctionnalité détaillée :**
  - Vérifie le destinataire du message :
    - Si destinataire `"ALL"` ou non spécifié, distribue à tous les agents.
    - Sinon, transmet explicitement le message à l’agent spécifié.

---

### Méthode : `envoyer_prompt_initial(self)`

- **Fonctionnalité détaillée :**
  - Envoie automatiquement le prompt initial spécifié à tous les agents au début des interactions.
  - Marque ce message comme non mémorisé pour éviter toute surcharge inutile.
  - Affiche une confirmation en mode verbeux.

---

### Méthode : `run(self)`

- **Fonctionnalité détaillée :**
  - Lance explicitement les interactions pour le nombre de tours (`n_rounds`) spécifié.
  - Envoie d’abord le prompt initial (si fourni).
  - Coordonne chaque tour, chaque agent traitant ses messages entrants.
  - Affiche explicitement le numéro de chaque tour en cours en mode verbeux.
  - Affiche un message final indiquant la fin des interactions.

---

### Méthode : `step(self)`

- **Fonctionnalité détaillée :**
  - Réalise explicitement un seul tour d’interaction, utile pour des traitements progressifs ou itératifs.

---

## 💻 Interface CLI directe (`if __name__ == "__main__"`)

Permet de lancer directement une équipe depuis la ligne de commande.

- **Imports :**
  - `argparse` : pour gérer les arguments passés via la CLI.

- **Arguments CLI :**
  - `--agents` *(obligatoire)* : Liste des noms d’agents à instancier automatiquement.
  - `prompt` *(obligatoire)* : Prompt initial déclenchant les interactions autonomes.
  - `--n_rounds` : Nombre de tours d’interactions (défaut=5).
  - `--verbose` : Active explicitement le mode détaillé.

- **Fonctionnement détaillé en CLI :**
  - Instanciation automatique des agents via `BaseAgent`, avec un rôle par défaut (`BaseRole`).
  - Création et lancement explicite de l’équipe avec les paramètres fournis.
  - Coordonne automatiquement les interactions des agents créés via l’interface CLI.

---