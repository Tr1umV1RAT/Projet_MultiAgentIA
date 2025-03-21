import unittest
from roles.base_role import BaseRole
from skills.reasoning import Reasoning
from skills.communication.messages import Message

# Dummy classes pour simuler un agent, un rôle et une mémoire

class DummyMemory:
    def __init__(self):
        self.history = []

    def get_recent_history(self, limit=3):
        # Retourne les derniers messages de l'historique sous forme de chaîne.
        if self.history:
            return "\n".join(self.history[-limit:])
        return ""

class DummyRole(BaseRole):
    def __init__(self):
        super().__init__(
            nom_role="Dummy",
            objectif="Tester l'intégration du rôle dans le prompt.",
            contexte="Contexte de test.",
            instructions_specifiques="Aucune instruction supplémentaire."
        )

class DummyAgent:
    def __init__(self, name, role=None):
        self.name = name
        self.role = role
        # Simuler la mémoire de l'agent avec une instance de DummyMemory.
        self.memoire = DummyMemory()

class TestReasoning(unittest.TestCase):
    def test_reflechir_with_memory(self):
        """
        Vérifie que reflechir() génère un prompt enrichi incluant l'historique
        et que le message de réponse est bien construit.
        """
        role = DummyRole()
        agent = DummyAgent("TestAgent", role)
        # Simuler une mémoire non vide
        agent.memoire.history = ["Message 1", "Message 2", "Message 3"]
        
        reasoning = Reasoning(agent)
        # Patch de la méthode run() de l'outil LLM pour retourner une réponse prédéfinie.
        reasoning.llm_tool.run = lambda prompt: f"Réponse simulée pour: {prompt}"
        
        # Créer le message d'entrée via la factory
        input_msg = Message.create(expediteur="User", destinataire=agent.name, contenu="Quel est le problème ?", dialogue=True)
        response_msg = reasoning.reflechir(input_msg)
        
        # Construire le prompt attendu
        base_prompt = role.generer_prompt("Quel est le problème ?")
        expected_history = "Message 1\nMessage 2\nMessage 3"
        expected_prompt = f"{base_prompt}\nHistorique récent:\n{expected_history}\n"
        expected_response = f"Réponse simulée pour: {expected_prompt}"
        
        self.assertEqual(response_msg.contenu, expected_response)
        self.assertEqual(response_msg.expediteur, agent.name)
        self.assertEqual(response_msg.destinataire, "User")
        self.assertEqual(response_msg.meta.get("original_prompt"), expected_prompt)

    def test_reflechir_without_memory(self):
        """
        Vérifie que reflechir() génère le prompt sans ajout d'historique si la mémoire est vide.
        """
        role = DummyRole()
        agent = DummyAgent("TestAgent", role)
        # S'assurer que la mémoire est vide
        agent.memoire.history = []
        
        reasoning = Reasoning(agent)
        reasoning.llm_tool.run = lambda prompt: f"Réponse simulée pour: {prompt}"
        
        input_msg = Message.create(expediteur="User", destinataire=agent.name, contenu="Quel est le problème ?", dialogue=True)
        response_msg = reasoning.reflechir(input_msg)
        
        base_prompt = role.generer_prompt("Quel est le problème ?")
        expected_prompt = base_prompt  # Pas d'historique ajouté
        expected_response = f"Réponse simulée pour: {expected_prompt}"
        
        self.assertEqual(response_msg.contenu, expected_response)
        self.assertEqual(response_msg.expediteur, agent.name)
        self.assertEqual(response_msg.destinataire, "User")
        self.assertEqual(response_msg.meta.get("original_prompt"), expected_prompt)

if __name__ == '__main__':
    unittest.main()
