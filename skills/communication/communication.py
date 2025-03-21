from skills.communication.messages import Message
from typing import Callable, List

class Communication:
    """
    Skill de communication qui peut être utilisé de manière autonome par un agent
    ou injecté dans une team pour centraliser la distribution des messages.
    Une callback de routage (route_callback) peut être définie pour permettre
    de diffuser les messages aux autres agents dans une équipe.
    """
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.outbox: List[Message] = []  # Historique des messages envoyés.
        self.route_callback: Callable[[Message], None] = None

    def set_route_callback(self, callback: Callable[[Message], None]):
        """Définit la callback de routage pour distribuer les messages."""
        self.route_callback = callback

    def envoyer(self, message: Message):
        """Enregistre le message et l'envoie via la callback (si définie)."""
        self.outbox.append(message)
        if self.verbose or message.affichage_force or message.dialogue:
            dest = message.destinataire if isinstance(message.destinataire, str) else "multiple"
            print(f"[{message.expediteur} -> {dest}] {message.contenu}")
        if self.route_callback:
            self.route_callback(message)

    def afficher_messages_visibles(self):
        """Affiche tous les messages dans l'historique qui sont marqués dialogue ou affichage_force."""
        for msg in self.outbox:
            if msg.dialogue or msg.affichage_force:
                if msg.destinataire is None or (isinstance(msg.destinataire, str) and msg.destinataire.lower() in {"all", "tous"}):
                    dest_label = "TOUS"
                elif isinstance(msg.destinataire, (list, tuple, set)):
                    dest_label = ", ".join([d if isinstance(d, str) else (getattr(d, "name", None) or str(d))
                                             for d in msg.destinataire])
                else:
                    dest_label = msg.destinataire if isinstance(msg.destinataire, str) else (getattr(msg.destinataire, "name", None) or str(msg.destinataire))
                print(f"[{msg.expediteur} -> {dest_label}] {msg.contenu}")
