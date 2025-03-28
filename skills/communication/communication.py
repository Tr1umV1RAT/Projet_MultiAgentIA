# skills/communication/communication.py
from skills.communication.messages import Message

class Communication:
    def __init__(self, agents=None, verbose=False, route_callback=None):
        self.agents = agents if agents is not None else []
        self.verbose = verbose
        self.route_callback = route_callback
        self.outbox = []

    def send(self, message):
        if not isinstance(message, Message):
            try:
                message = Message.create(message)
            except Exception as e:
                raise ValueError("Impossible de convertir l'entrée en instance de Message") from e

        self.outbox.append(message)

        # ✅ Rendu clair et utile :
        #if self.verbose and (message.dialogue or message.affichage_force):
         #   print(f"🗨️  {message.origine} → {message.destinataire} : {message.contenu[:500]}")

        if self.route_callback:
            self.route_callback(message)
        elif self.agents:
            if message.destinataire.upper() == "ALL":
                for agent in self.agents:
                    if agent.name != message.origine:
                        agent.messages.append(message)
            else:
                destinataire_trouve = False
                for agent in self.agents:
                    if agent.name == message.destinataire:
                        agent.messages.append(message)
                        destinataire_trouve = True
                        break
                if not destinataire_trouve and self.verbose:
                    print(f"Aucun agent trouvé pour le destinataire : {message.destinataire}")
    def envoyer(self, message):
        """
        Alias rétrocompatible de `send`.
        """
        return self.send(message)
    def ajouter_agent(self, agent):
        self.agents.append(agent)


   
    def set_route_callback(self, callback):
        self.route_callback = callback
    
    def afficher_messages_visibles(self):
        print("\n--- Historique des messages envoyés ---")
        for msg in self.outbox:
            if msg.dialogue or msg.affichage_force:
                print(msg)
