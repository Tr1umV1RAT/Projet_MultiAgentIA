import re
import uuid
from agents.base_agent import BaseAgent
from roles.codeur import Codeur  # Assure-toi que ce rôle est défini dans roles/codeur.py
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.communication.communication import Communication
from skills.db_management.db_management import DBManagementSkill
from skills.reasoning import Reasoning
from config import Config
from skills.communication.messages import Message

class AgentCodeur(BaseAgent):
    def __init__(self, nom="AgentCodeur", role=None, memoire_persistante=None):
        role = role or Codeur()
        self.memoire_court_terme = ShortTermMemory()
        self.communication = Communication()
        # Crée l'instance de LongTermMemory pour la persistance
        self.memoire_persistante = memoire_persistante or LongTermMemory(
            db_name="codeur_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            description="Mémoire persistante de l'agent codeur"
        )
        # Passe la connexion existante de la mémoire à DBManagementSkill
        self.db_skill = DBManagementSkill(
            db_name="codeur_memory.db",
            schema=Config.MEMORY_TABLE_SCHEMA,
            connexion=self.memoire_persistante.connexion
        )
        skills = [self.memoire_court_terme, self.communication, self.db_skill, self.memoire_persistante]
        super().__init__(name=nom, role=role, skills=skills)

    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.contenu, str):
            return Message.create(
                expediteur=self.name,
                destinataire=message.expediteur,
                contenu="Message non valide ou vide. Merci de reformuler.",
                meta={"error": "invalid_message"},
                dialogue=True
            )

        prompt = f"""
Tu es un codeur expert, rigoureux, et ton travail est destiné à être relu par un reviewer. Tu dois générer un code parfaitement documenté, propre, modulaire et testé. Voici les consignes strictes :

1. Tu ne produis que du **code Python**.
2. Tu **encadres obligatoirement** ton code dans un bloc Markdown avec le format ```python.
3. Tu ne produis **aucun commentaire hors du code**. Aucun texte d'explication, uniquement du code.
4. Tu gères la production d'un code fonctionnel, directement exécutable.
5. Le nom du fichier doit être précisé sous la forme suivante : `# fichier: nom_fichier.py` en première ligne si applicable.
6. Chaque fonction ou classe est documentée via une docstring en français.
7. Tu évites les bibliothèques inutiles. Si tu en utilises, elles doivent être standards ou mentionnées comme nécessaires.
8. Le code doit respecter les conventions PEP8.

Tâche reçue :
{message.contenu}
"""
        llm_input = Message.create(
            expediteur=self.name,
            destinataire=self.name,
            contenu=prompt,
            meta={"instruction": "code_request"}
        )
        result_message = self.reasoning.reflechir(llm_input)
        generated_code = result_message.contenu
        code_block = re.search(r"```python\n(.*?)```", generated_code, re.DOTALL)
        filename_line = re.search(r"# fichier: (.*?\.py)", generated_code)
        code_cleaned = code_block.group(1).strip() if code_block else generated_code.strip()
        filename = filename_line.group(1) if filename_line else f"{uuid.uuid4().hex[:8]}.py"
        self.db_skill.save_message(Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=code_cleaned,
            meta={"type_message": "code", "task": message.contenu, "action": "save_code", "filename": filename},
            dialogue=False
        ))
        return Message.create(
            expediteur=self.name,
            destinataire=message.expediteur,
            contenu=f"Code généré et stocké sous le nom {filename}.",
            meta={"filename": filename},
            dialogue=True
        )