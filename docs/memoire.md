# 🧠 Mémoire dans le système MultiAgentIA

La mémoire est un composant fondamental du projet MultiAgentIA. Elle permet aux agents de raisonner sur des faits passés, de réutiliser leur propre historique, de croiser des informations avec d'autres agents et de filtrer leur contexte de travail de manière dynamique.

---

## 🔁 Structure de la mémoire

Chaque agent possède **trois niveaux de mémoire** :

### 1. Mémoire à court terme (`ShortTermMemory`)
- Structure : buffer circulaire en RAM (non persistante)
- Contenu : derniers `Message` reçus ou produits par l’agent
- Utilité : permet de maintenir un « contexte local » pour générer des réponses cohérentes
- Capacité par défaut : 10 messages (modifiable)

### 2. Mémoire à long terme (`LongTermMemory`)
- Stockage : base SQLite persistante par agent
- Chemin : `agent_memories/NOM_TIMESTAMP/long_term_memory.db`
- Contenu : messages sélectionnés selon leur **importance**
- Accès : via filtrage, requêtes, inspection, ou appels LLM
- Protection : journal des accès en lecture (`memory_access_log.db`)

### 3. Mémoire de travail (ou mémoire immédiate)
- Contenu : sous-ensemble de souvenirs pertinents extraits de la mémoire longue
- Générée à chaque itération par appel au LLM (via `query()` sur la base)
- Injectée dans le prompt du LLM à chaque décision de l’agent

---

## 🔐 Mécanisme de filtrage : importance et mémorisation

Chaque `Message` contient :
- `importance` : de 1 à 10, fixée automatiquement ou manuellement
- `memoriser` : booléen, permet d’interdire la conservation même si important

### Exemple :
```python
Message(
    origine="user",
    destinataire="agent",
    contenu="Mot de passe : hunter2",
    importance=9,
    memoriser=True
)
```

---

## 🧠 Fonctionnement du `MemorySkill`

Le `MemorySkill` est un module central de chaque agent, qui orchestre :
1. L’enregistrement de messages importants dans la mémoire longue
2. La génération du contexte de travail (mémoire immédiate)
3. La notation automatique des messages via LLM (si `importance=None`)
4. Le pruning : oubli automatique des souvenirs trop anciens ou trop peu importants

---

## 🧪 Interrogation réflexive : `MemoryInspectorSkill`

Un agent peut interroger sa propre mémoire pour :
- Dresser un résumé
- Identifier des événements marquants
- Distinguer les périodes actives

> À terme, tous les agents devraient disposer d’un mécanisme de réflexivité leur permettant d’analyser leur propre fonctionnement.

---

## 🧑‍🤝‍🧑 Accès croisé à la mémoire

Un agent peut accéder à la mémoire longue d’un autre via le `MemoryAccessSkill` (ou module utilitaire `memory_access.py`) :
- Requête filtrée (importance, type, date, etc.)
- Logguée automatiquement dans un journal d’accès
- Protégée par convention (chaque agent peut refuser certains accès via des règles locales)

---

## 🧹 Nettoyage automatique : oubli contrôlé

Un appel à `prune()` sur une mémoire longue :
- Supprime toutes les entrées au-delà d’un certain seuil (ex : 500 dernières seulement)
- Se fait automatiquement à chaque insertion si la taille maximale est atteinte

---

## 📋 Inspection manuelle

Deux outils CLI sont disponibles pour l’humain :
- `memory_viewer.py` → afficher les souvenirs pertinents d’un agent (filtrage par type / importance)
- `memory_log_viewer.py` → afficher les requêtes d’accès aux bases mémoire

---

## 🚧 À venir

- Mémoire multi-agents partagée
- Indexation sémantique des souvenirs (tags dynamiques)
- Mécanisme d’oubli actif (pas seulement passif)
- Codage émotionnel (importance non seulement cognitive mais affective)

---

## ✅ Résumé

La mémoire dans MultiAgentIA est un pilier de la cognition des agents. Sa gestion repose sur :
- une sélection automatique ou explicite des messages
- une capacité d’oubli
- une interopérabilité entre agents
- une intégration directe au raisonnement (via les prompts LLM)

Elle est en constante évolution et peut devenir un vecteur d’identité pour chaque agent.

