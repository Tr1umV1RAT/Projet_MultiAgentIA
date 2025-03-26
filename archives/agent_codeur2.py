# agents/agent_codeur.py

import re
import uuid
from agents.base_agent import BaseAgent
from roles.codeur import CodeurRole  # Assurez-vous que ce rôle existe et est correctement implémenté
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message
from tools.project_io import save_code_file  # Cette fonction doit être définie dans tools/project_io.py

class AgentCodeur(BaseAgent):
    def __init__(self, nom="AgentCodeur", role=None, memoire_persistante=None, project_path=".", verbose=False):
        # Utilisation du rôle par défaut CodeurRole
        role = role or CodeurRole()
        self.verbose = verbose
        
        # Initialisation des skills de mémoire et de communication
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication(verbose=verbose)
        
        # Pour éviter la création multiple de DB, on partage la même instance de mémoire persistante
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="codeur_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante de l'agent codeur"
        )
        # On passe la connexion existante afin de ne pas créer une nouvelle DB dans DBManagementSkill
        self.db_skill = DBManagementSkill(
            db_name="codeur_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            connexion=self.memoire_persistante.connexion
        )
        
        self.project_path = project_path
        
        # Regrouper tous les skills
        skills = [self.memoire_court_terme, self.communication, self.db_skill, self.memoire_persistante]
        super().__init__(name=nom, role=role, skills=skills)
        
        # Instanciation du module de raisonnement
        self.reasoning = Reasoning(self)
        
        if self.verbose:
            print(f"[{self.name} INIT] Mode verbeux activé. Dossier projet : {self.project_path}")

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            error_msg = "Message non valide ou vide reçu. Merci de reformuler la tâche à effectuer."
            if self.verbose:
                print(f"[{self.name} ERROR] {error_msg}")
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu=error_msg,
                meta={"error": "Invalid message"}
            )
        
        # Construction du prompt pour générer du code Python conforme aux exigences
        prompt = f""" 
Tu es un codeur expert et rigoureux. Ton travail doit être relu par un reviewer.
Génère un code Python production-ready, parfaitement documenté, propre, modulaire et testé.
Respecte strictement ces consignes :
1. Tu produis uniquement du **code Python**.
2. Le code doit être entièrement contenu dans un bloc Markdown au format ```python.
3. Aucun commentaire ou explication ne doit apparaître en dehors du bloc de code.
4. Le code doit être fonctionnel et exécutable directement.
5. Les fonctions doivent êtres écrites en intégralité.
6. Si le type de projet nécessite un scenario, il est partagé par un autre membre de l'équipe. 
7. Si un scenario est partagé par un autre membre de l'équipe, il doit être intégré directement dans le code.
8. Si applicable, indique le nom du fichier dans la première ligne sous la forme : `# fichier: nom_fichier.py`.
9. Chaque fonction/classe doit être documentée avec une docstring en français.
10. Utilise uniquement des bibliothèques standards, sauf mention contraire.
11. Le code doit être conforme à PEP8.

Tâche à réaliser :
{message.contenu}
"""
        if self.verbose:
            print(f"[{self.name} DEBUG] Prompt envoyé au module de reasoning :\n{prompt}\n")
        
        # Création d'un message pour le module de reasoning
        llm_input = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "code_request"}
        )
        result_message = self.reasoning.reflechir(llm_input)
        generated_code = result_message.contenu
        
        if self.verbose:
            print(f"[{self.name} DEBUG] Code généré par le reasoning :\n{generated_code}\n")
        
        # Extraction du bloc de code et du nom du fichier (si présent)
        code_block_match = re.search(r"```python\n(.*?)```", generated_code, re.DOTALL)
        filename_match = re.search(r"# fichier: (.*?\.py)", generated_code)
        code_cleaned = code_block_match.group(1).strip() if code_block_match else generated_code.strip()
        filename = filename_match.group(1).strip() if filename_match else f"{uuid.uuid4().hex[:8]}.py"
        
        # Sauvegarde du code généré dans le dossier du projet
        save_code_file(filename, code_cleaned, self.project_path)
        
        if self.verbose:
            print(f"[{self.name} INFO] Code sauvegardé sous : {self.project_path}/{filename}")
        
        # Enregistrement de la génération dans la base via le skill de DB
        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Code généré et sauvegardé sous le nom {filename}.",
            meta={"type_message": "code", "filename": filename, "task": message.contenu}
        ))
        
        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Code généré et sauvegardé sous le nom {filename}.",
            meta={"filename": filename}
        )