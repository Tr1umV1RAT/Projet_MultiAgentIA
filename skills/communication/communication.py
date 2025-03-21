from skills.base_skill import BaseSkill
from skills.communication.messages import Message
from config import Config
from skills.db_management.db_management import DBManagementSkill
class Communication(BaseSkill):
    def __init__(self):
        super().__init__("Communication")
        self.file_messages = []

    def envoyer(self, message: Message):
        """Ajoute le message à la file de communication."""
        self.file_messages.append(message)
        if Config.verbose or message.affichage_force:
            print(f"[{message.origine}] ➡️ [{message.destinataire}] : {message.contenu}")

    def recevoir(self, destinataire):
        # Copie explicite de la liste pour éviter les erreurs lors de la suppression
        messages_recus = messages_recus = [m for m in self.file_messages if m.destinataire in (destinataire if isinstance(destinataire, str) else destinataire.nom, "tous")].copy()  # ➡️ FAIRE UNE COPIE EXPLICITE

        for message in messages_recus:
            nom_destinataire = destinataire if isinstance(destinataire, str) else destinataire.nom

            if Config.verbose or message.affichage_force:
                print(f"[{nom_destinataire}] reçoit : '{message.contenu}' (de {message.origine})")

            if message.memoriser:
                if hasattr(destinataire, "memoire"):
                    destinataire.memoire.save(
                        contenu=message.contenu,
                        agent_name=message.origine,
                        type_info=message.type_message
                    )

                if hasattr(destinataire, "memoire_persistante"):
                    destinataire.memoire_persistante.save_message(message)

            if message.action and hasattr(destinataire, 'outils'):
                if message.action in destinataire.outils:
                    resultat_action = destinataire.outils[message.action].run(message.contenu)
                    self.envoyer(Message(
                        origine=destinataire.nom,
                        destinataire=message.origine,
                        contenu=resultat_action,
                        affichage_force=message.affichage_force,
                        memoriser=message.memoriser,
                        type_message=f"resultat_{message.action}"
                    ))

            if message.dialogue and hasattr(destinataire, "raisonnement"):
                prompt_final = (
                    destinataire.role.generer_prompt(message.contenu)
                    if destinataire.role else message.contenu
                )
                reponse = destinataire.raisonnement.reflechir(prompt_final)

                self.envoyer(Message(
                    origine=destinataire.nom,
                    destinataire=message.origine,
                    contenu=reponse,
                    affichage_force=message.affichage_force,
                    type_message="dialogue",
                    memoriser=message.memoriser
                ))

            if hasattr(destinataire, "recevoir_message"):
                destinataire.recevoir_message(message)

            # Retrait explicite, sécurisé (message existe encore)
            if message in self.file_messages:
                self.file_messages.remove(message)


