from skills.communication.communication import Communication
from skills.communication.messages import Message
from skills.memory.short_term import ShortTermMemory
from skills.memory.long_term import LongTermMemory
from skills.reasoning import Reasoning
from config import Config

class BaseAgent:
    def __init__(self, nom="Agent", role=None, memoire_persistante=None):
        self.nom = nom
        self.role = role
        self.communication = Communication()
        self.memoire = ShortTermMemory()
        self.memoire_persistante = memoire_persistante
        self.raisonnement = Reasoning()
        self.outils = {outil.name: outil for outil in role.outils} if role else {}

    def __call__(self, prompt):
        message = Message(
            origine="Utilisateur",
            destinataire=self.nom,
            contenu=prompt,
            affichage_force=True,
            dialogue=True
        )
        self.communication.envoyer(message)
        self.communication.recevoir(self)

    def recevoir_message(self, message: Message):
        if message.type_message == "outil":
            nom_outil, query = message.contenu.split(":", 1)
            outil = self.outils.get(nom_outil.strip())
            if outil:
                resultat = outil.run(query)
                message_reponse = Message(
                    origine=self.nom,
                    destinataire="Utilisateur",
                    contenu=resultat,
                    affichage_force=True,
                    type_message="resultat_outil"
                )
                if self.memoire_persistante:
                    self.memoire_persistante.save_message(message_reponse)
            else:
                message_reponse = Message(
                    origine=self.nom,
                    destinataire="Utilisateur",
                    contenu=f"L'outil {nom_outil} n'est pas disponible.",
                    affichage_force=True
                )
        else:
            prompt_final = self.role.generer_prompt(message.contenu) if self.role else message.contenu
            # Utilisation de l'adaptateur LLM (injection via rôle ou directe selon la config)
            if Config.LLM_INJECTION_MODE == "role" and "LLM" in self.outils:
                reponse = self.outils["LLM"].run(prompt_final)
            else:
                reponse = self.raisonnement.reflechir(prompt_final)
            message_reponse = Message(
                origine=self.nom,
                destinataire=message.origine,
                contenu=reponse,
                affichage_force=True,
                type_message="dialogue"
            )
            if self.memoire_persistante:
                self.memoire_persistante.save_message(message_reponse)
            self.communication.envoyer(message_reponse)
