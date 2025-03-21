from agents.base_agent import BaseAgent
from roles.codeur_basique import CodeurBasique
from skills.coder import CoderSkill
from skills.memory.long_term import LongTermMemory
from config import Config

class AgentCodeur(BaseAgent):
    def __init__(self, nom="AgentCodeur", role=None, memoire_persistante=None):
        
        if role is None:
            role = CodeurBasique()  # le rôle de base explicitement utilisé si aucun autre n'est fourni

        super().__init__(
            nom=nom,
            role=role,
            memoire_persistante=memoire_persistante or LongTermMemory("codeur_memory.db", Config.MEMORY_TABLE_SCHEMA)
        )

        # Attribution explicite du skill de coder à l'agent (et non au rôle)
        self.skill_coder = CoderSkill()

    def recevoir_message(self, message: Message):
        # On traite explicitement le cas spécifique où l'agent est sollicité pour coder :
        if message.type_message == "demande_code":
            code_demande = message.contenu

            # L'agent utilise explicitement le skill CoderSkill
            code = self.skill_coder.generer_code(code_demande)

            message_reponse = Message(
                origine=self.nom,
                destinataire=message.origine,
                contenu=code,
                affichage_force=True,
                type_message="code"
            )

            # Enregistrement explicite dans la mémoire persistante
            if self.memoire_persistante:
                self.memoire_persistante.save_message(message_reponse)

            self.communication.envoyer(message_reponse)
            self.communication.recevoir(message.origine)

        else:
            # Sinon, comportement par défaut défini par BaseAgent
            super().recevoir_message(message)
