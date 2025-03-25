# skills/communication/communication.py
from skills.communication.messages import Message

class Communication:
    def __init__(self, agents=None, verbose=False, route_callback=None):
        self.agents = agents if agents is not None else []
        self.verbose = verbose
        self.route_callback = route_callback
        self.outbox = []

    def envoyer(self, message):
        # Vérifier et convertir le message en instance de Message
        if not isinstance(message, Message):
            try:
                message = Message.create(message)
            except Exception as e:
                raise ValueError("Impossible de convertir l'entrée en instance de Message") from e

        self.outbox.append(message)
        if self.verbose:
            print(f"Envoi du message : {message}")

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

    def ajouter_agent(self, agent):
        self.agents.append(agent)
