import unittest
import io
import sys
from skills.communication.messages import Message
from skills.communication.communication import Communication

# Classe DummyAgent pour simuler un agent
class DummyAgent:
    def __init__(self, name):
        self.name = name
        self.messages = []  # File de réception des messages
        self.communication = None

    def process_messages(self):
        # Pour le test, on vide simplement la file de messages après traitement
        self.messages = []

class TestCommunication(unittest.TestCase):
    def setUp(self):
        # Créer quelques agents simulés
        self.agent_alice = DummyAgent("Alice")
        self.agent_bob = DummyAgent("Bob")
        self.agent_charlie = DummyAgent("Charlie")
        self.agents = [self.agent_alice, self.agent_bob, self.agent_charlie]
        # Créer une instance de Communication en mode non verbose par défaut
        self.comm = Communication(self.agents, verbose=False)

    def test_send_private_message(self):
        # Envoyer un message privé de Alice à Bob
        msg = Message.create(expediteur="Alice", destinataire="Bob", contenu="Hello Bob!", dialogue=False)
        self.comm.envoyer(msg)
        # Bob doit recevoir le message
        self.assertIn(msg, self.agent_bob.messages)
        # Les autres agents ne doivent pas le recevoir
        self.assertNotIn(msg, self.agent_alice.messages)
        self.assertNotIn(msg, self.agent_charlie.messages)
        # L'historique global doit contenir le message
        self.assertIn(msg, self.comm.history)

    def test_send_broadcast_message(self):
        # Envoyer un message broadcast (destinataire "ALL")
        msg = Message.create(expediteur="Alice", destinataire="ALL", contenu="Hello everyone!", dialogue=False)
        self.comm.envoyer(msg)
        # Tous les agents doivent recevoir le message
        for agent in self.agents:
            self.assertIn(msg, agent.messages)
        # L'historique global doit contenir le message
        self.assertIn(msg, self.comm.history)

    def test_send_dialogue_message(self):
        # Envoyer un message privé de Alice à Bob, marqué comme dialogue
        msg = Message.create(expediteur="Alice", destinataire="Bob", contenu="Let's discuss the issue.", dialogue=True)
        self.comm.envoyer(msg)
        # Bob doit recevoir le message (destinataire principal)
        self.assertIn(msg, self.agent_bob.messages)
        # Les autres agents (sauf l'expéditeur) doivent aussi le recevoir en copie
        self.assertNotIn(msg, self.agent_alice.messages)
        self.assertIn(msg, self.agent_charlie.messages)
        # L'historique global doit contenir le message
        self.assertIn(msg, self.comm.history)

    def test_verbose_output(self):
        # Vérifier que le message est affiché en mode verbose
        msg = Message.create(expediteur="Alice", destinataire="Bob", contenu="Debug message", dialogue=True)
        # Capturer la sortie standard
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Activer le mode verbose
        self.comm.verbose = True
        self.comm.envoyer(msg)
        self.comm.afficher_messages_visibles()

        # Restaurer stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("[Alice -> Bob]", output)
        self.assertIn("Debug message", output)

if __name__ == '__main__':
    unittest.main()
