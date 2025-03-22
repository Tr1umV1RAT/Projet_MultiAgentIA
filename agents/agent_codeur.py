from agents.base_agent import BaseAgent
from skills.memory.short_term import ShortTermMemory
from skills.communication import CommunicationSkill
from skills.db_management import DBManager
from messages import Message
from skills.reasoning import Reasoning 
import re
import uuid

class AgentCodeur(BaseAgent):
    def __init__(self, nom="AgentCodeur", role=None, memoire_persistante=None):
        
        if role is None:
            from roles import codeur
            role = Codeur()  # le rôle de base explicitement utilisé si aucun autre n'est fourni

        super().__init__(
            nom=nom,
            role=role,
            memoire_persistante=memoire_persistante or LongTermMemory("codeur_memory.db", Config.MEMORY_TABLE_SCHEMA)
        )

        
        
    def process_message(self, message: Message) -> Message:
        if not message or not isinstance(message.content, str):
            return Message(
                sender=self.nom,
                recipient=message.sender,
                content="Message non valide ou vide reçu. Merci de reformuler la tâche à effectuer.",
                metadata={"error": "Invalid message"}
            )

        # Prompt ultra strict pour la génération de code
        prompt = f""" 
Tu es un codeur expert, rigoureux, et ton travail est destiné à être relu par un reviewer. Tu dois générer un code parfaitement documenté, propre, modulaire et testé. Voici les consignes strictes :

1. Tu ne produis que du **code Python**.
2. Tu **encadres obligatoirement** ton code dans un bloc Markdown avec le format ```python.
3. Tu ne produis **aucun commentaire hors du code**. Aucun texte d'explication, uniquement du code.
4. Tu génères un code **fonctionnel**, que l'on puisse copier-coller et exécuter sans modification.
5. Le nom du fichier doit être précisé sous la forme suivante : `# fichier: nom_fichier.py` en première ligne si applicable.
6. Chaque fonction ou classe est documentée via une docstring en français.
7. Tu évites les bibliothèques inutiles. Si tu en utilises, elles doivent être standards ou mentionnées comme nécessaires.
8. Le code doit respecter les conventions PEP8.

Tâche reçue :
{message.content}
"""

        generated_code =  Reasoning(prompt)# À remplacer par llm_adapter.call(prompt)

        # Extraction du code et nom de fichier
        code_block = re.search(r"```python\n(.*?)```", generated_code, re.DOTALL)
        filename_line = re.search(r"# fichier: (.*?\.py)", generated_code)

        code_cleaned = code_block.group(1).strip() if code_block else generated_code
        filename = filename_line.group(1) if filename_line else f"{uuid.uuid4().hex[:8]}.py"

        # Sauvegarde dans la base
        db = self.get_skill(DBManager)
        db.store_message({
            "type": "code",
            "filename": filename,
            "content": code_cleaned,
            "task": message.content,
            "author": self.nom
        })

        return Message(
            sender=self.nom,
            recipient=message.sender,
            content=f"Code généré et stocké sous le nom {filename}.",
            metadata={"filename": filename}
        )

    def _mock_llm(self, prompt: str) -> str:
        # Simulation temporaire pour dev
        return (
            "# fichier: mon_script.py\n"
            "```python\n"
            "def dire_bonjour(nom):\n"
            "    \"\"\"\n"
            "    Affiche un message de salutation personnalisé.\n"
            "    :param nom: str - le nom de la personne à saluer\n"
            "    \"\"\"\n"
            "    print(f\"Bonjour, {nom} !\")\n"
            "```"
        )
