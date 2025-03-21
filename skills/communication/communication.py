from skills.communication.message import Message
from typing import List

class Communication:
    """Système de communication asynchrone gérant la distribution des messages entre agents."""
    def __init__(self, agents, verbose: bool = False):
        """
        Initialise la communication avec les agents participants.
        - agents : liste ou dictionnaire des agents de l'équipe.
        - verbose : si True, active le mode verbeux (affichage de tous les messages de dialogue).
        """
        self.agents = {}       # Dictionnaire nom -> agent pour accès rapide par nom.
        # Enregistrer les agents dans le dictionnaire.
        if isinstance(agents, dict):
            for name, ag in agents.items():
                self.agents[name] = ag
        else:
            for ag in agents:
                # Utilise l'attribut 'name' ou 'nom' s'il existe, sinon une représentation par défaut.
                name = getattr(ag, "name", None) or getattr(ag, "nom", None) or str(ag)
                self.agents[name] = ag
        
        # Initialiser la file de messages pour chaque agent et attribuer la référence Communication.
        for name, ag in self.agents.items():
            ag.messages = []  # S'assurer que la file est vide.
            ag.communication = self
        
        self.history: List[Message] = []  # Historique de tous les messages envoyés.
        self.verbose = verbose

    def envoyer(self, message: Message):
        """
        Envoie un message dans la/les file(s) appropriées, selon le destinataire et les meta-données.
        - message: instance de Message à transmettre.
        """
        # Normaliser l'expéditeur en une chaîne de caractères.
        if not isinstance(message.expediteur, str):
            exp_name = getattr(message.expediteur, "name", None) or getattr(message.expediteur, "nom", None)
            message.expediteur = exp_name if exp_name else str(message.expediteur)
        
        # Ajouter le message à l'historique global.
        self.history.append(message)
        
        # Déterminer les destinataires principaux.
        dest = message.destinataire
        if dest is None or (isinstance(dest, str) and dest.lower() in {"all", "tous"}):
            destinataires_principaux = list(self.agents.keys())
        elif isinstance(dest, (list, tuple, set)):
            destinataires_principaux = []
            for d in dest:
                if isinstance(d, str) and d in self.agents:
                    destinataires_principaux.append(d)
                else:
                    nom = getattr(d, "name", None) or getattr(d, "nom", None)
                    if nom and nom in self.agents:
                        destinataires_principaux.append(nom)
        else:
            if isinstance(dest, str) and dest in self.agents:
                destinataires_principaux = [dest]
            else:
                nom = getattr(dest, "name", None) or getattr(dest, "nom", None)
                destinataires_principaux = [nom] if (nom and nom in self.agents) else []
        
        # Éliminer les doublons tout en préservant l'ordre.
        destinataires_principaux = list(dict.fromkeys(destinataires_principaux))
        
        # Distribuer le message aux destinataires principaux (file de réception de chaque agent).
        for name in destinataires_principaux:
            self.agents[name].messages.append(message)
        
        # Si le message est marqué visible (dialogue public ou affichage forcé), le distribuer aux autres agents.
        if message.dialogue or message.affichage_force:
            for name, agent in self.agents.items():
                if name in destinataires_principaux or name == message.expediteur:
                    continue  # Ne pas dupliquer pour le destinataire principal ou l'expéditeur.
                agent.messages.append(message)
        
        # Affichage conditionnel du message selon le mode verbeux et le flag affichage_force.
        if message.affichage_force or (message.dialogue and self.verbose):
            # Construction d'une étiquette lisible pour le destinataire.
            if dest is None or (isinstance(dest, str) and dest.lower() in {"all", "tous"}):
                dest_label = "TOUS"
            elif isinstance(dest, (list, tuple, set)):
                dest_noms = []
                for d in dest:
                    if isinstance(d, str):
                        dest_noms.append(d)
                    else:
                        nom = getattr(d, "name", None) or getattr(d, "nom", None) or str(d)
                        dest_noms.append(nom)
                dest_label = ", ".join(dest_noms)
            else:
                dest_label = dest if isinstance(dest, str) else (getattr(dest, "name", None) or str(dest))
            print(f"[{message.expediteur} -> {dest_label}] {message.contenu}")

    def afficher_messages_visibles(self):
        """Affiche tous les messages dans l'historique ayant dialogue=True ou affichage_force=True."""
        for msg in self.history:
            if msg.dialogue or msg.affichage_force:
                if msg.destinataire is None or (isinstance(msg.destinataire, str) and msg.destinataire.lower() in {"all", "tous"}):
                    dest_label = "TOUS"
                elif isinstance(msg.destinataire, (list, tuple, set)):
                    dest_noms = []
                    for d in msg.destinataire:
                        if isinstance(d, str):
                            dest_noms.append(d)
                        else:
                            nom = getattr(d, "name", None) or getattr(d, "nom", None) or str(d)
                            dest_noms.append(nom)
                    dest_label = ", ".join(dest_noms)
                else:
                    dest_label = msg.destinataire if isinstance(msg.destinataire, str) else (getattr(msg.destinataire, "name", None) or str(msg.destinataire))
                print(f"[{msg.expediteur} -> {dest_label}] {msg.contenu}")
