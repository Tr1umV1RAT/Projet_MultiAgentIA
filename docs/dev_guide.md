# 🛠️ Guide du développeur – MultiAgentIA

Ce document est destiné aux contributeurs souhaitant ajouter de nouveaux composants à l’architecture MultiAgentIA : agents, rôles, skills, tools, teams.

---

## 🔧 Structure du projet

Le projet suit une architecture modulaire :

```
Projet_MultiAgentIA/
├── agents/              # Tous les agents IA
├── roles/               # Rôles attribués aux agents
├── skills/              # Capacités indépendantes (raisonnement, mémoire...)
├── tools/               # Outils spécialisés (LLM, scrapers...)
├── teams/               # Compositions d’agents (projets)
├── memory/              # Bases de données mémoire (par agent)
├── utils/               # Outils CLI, helpers
├── docs/                # Documentation
└── tests/               # Tests unitaires et fonctionnels
```

---

## 👤 Ajouter un agent

1. Créer une classe dans `agents/agent_monagent.py` :
```python
from agents.base_agent import BaseAgent
from roles.mon_role import MonRole

class AgentMonAgent(BaseAgent):
    def __init__(self):
        role = MonRole()
        super().__init__(name="MonAgent", role=role)
```
2. Le nom de l’agent sert à créer son dossier mémoire automatiquement.
3. Il dispose automatiquement de : LLM, Skills de base, Communication, Mémoire.

---

## 🎭 Ajouter un rôle

1. Créer une classe dans `roles/mon_role.py` :
```python
from roles.base_role import BaseRole

class MonRole(BaseRole):
    def __init__(self):
        objectif = "Effectuer une tâche X de façon autonome."
        super().__init__(name="MonRole", objectif=objectif)

    def get_prompt(self):
        return f"Tu es un agent ayant pour rôle : {self.name}. Ton objectif est : {self.objectif}."
```
2. Les prompts peuvent être enrichis dynamiquement.
3. Les `tools` peuvent être attribués au rôle.

---

## 🧠 Ajouter un skill

1. Créer un fichier dans `skills/` ou `skills/mon_skill/` :
```python
from skills.base_skill import BaseSkill

class MonSkill(BaseSkill):
    def __init__(self):
        super().__init__(name="MonSkill")

    def handle_message(self, message, agent):
        if message.type_message == "x":
            return ...  # Réponse ou action
```
2. Le skill peut être ajouté dans un agent via `self.skills.append(...)`

---

## 🛠️ Ajouter un tool

1. Créer un fichier Python dans `tools/mon_tool.py`
2. Un tool est une classe appelée par un skill ou un agent :
```python
class MonTool:
    def __init__(self, config):
        ...
    def search(self, query):
        ...
```
3. Le tool peut être injecté dans un skill ou passé dans un `Message`

---

## 🤖 Ajouter une team

1. Créer une classe dans `teams/mon_team.py` :
```python
from teams.base_team import BaseTeam
from agents.agent_codeur import AgentCodeur
from agents.agent_reviewer import AgentReviewer

class MonTeam(BaseTeam):
    def __init__(self, n_rounds=5):
        agents = {
            "Codeur": AgentCodeur(),
            "Reviewer": AgentReviewer(),
        }
        super().__init__(nom_team="MonTeam", agents=agents, n_rounds=n_rounds)
```
2. Les agents communiquent automatiquement via `Message`
3. La team peut être démarrée avec `.run()` ou `.step()`

---

## 🧪 Ajouter un test

Créer un fichier dans `tests/`, exemple `test_mon_skill.py` :
```python
from skills.mon_skill import MonSkill

def test_skill():
    skill = MonSkill()
    msg = Message(origine="test", destinataire="test", contenu="...")
    result = skill.handle_message(msg, agent=None)
    assert result is not None
```
Lance les tests depuis la racine :
```bash
pytest tests/
```

---

## 🔁 Fichiers importants à connaître

- `base_agent.py` : logique commune à tous les agents
- `base_role.py` : modèle de prompt et d’objectif
- `base_skill.py` : méthode `handle_message()`
- `base_team.py` : boucle de discussion en round
- `message.py` : tous les échanges transitent par `Message`
- `long_term.py` / `short_term.py` : gestion de la mémoire
- `llm_wrapper.py` : interface unifiée avec les LLM (local ou API)

---

## ✅ Bonnes pratiques

- Un agent = un nom unique = une mémoire isolée
- Toujours utiliser `Message` pour communiquer ou transmettre une action
- Ne jamais accéder à la mémoire d’un autre agent sans passer par `memory_access`
- Utiliser `verbose=True` pour le debug
- Documenter tout nouveau composant dans `docs/`

---

