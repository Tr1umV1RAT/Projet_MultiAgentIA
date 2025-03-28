import argparse
import sys
from agents.base_agent import BaseAgent
from skills.communication.messages import Message

# Mapping des types d'agents disponibles (peut être enrichi dynamiquement)
AGENT_TYPES = {
    "base_agent": BaseAgent,
    # Ajoute ici d'autres types d'agents si nécessaires (ex: "agent_codeur": AgentCodeur)
}

class BaseTeam:
    def __init__(self, agents, prompt, n_round=5, verbose=False):
        self.agents = agents
        self.initial_prompt = prompt
        self.n_round = n_round
        self.verbose = verbose
        self.history = []

    def run(self):
        if self.verbose:
            print("\n--- Début de la conversation ---\n")

        conversation_id = "team_convo"

        # Round 0 : envoyer le prompt initial à tous les agents
        system_message = Message(
            origine="système",
            destinataire="tous",
            contenu=self.initial_prompt,
            conversation_id=conversation_id
        )
        self.history.append(system_message)
        for agent in self.agents:
            agent.receive_message(system_message)

        # Rounds suivants : discussion entre agents
        for r in range(1, self.n_round + 1):
            if self.verbose:
                print(f"\n--- Round {r} ---")

            new_messages = []
            for agent in self.agents:
                last_message = self.history[-1] if self.history else system_message
                msg = Message(
                    origine="team",
                    destinataire=agent.name,
                    contenu=last_message.contenu,
                    conversation_id=conversation_id
                )
                response = agent.receive_message(msg)
                print(response.contenu)
                new_messages.append(response)

            self.history.extend(new_messages)

        if self.verbose:
            print("\n--- Fin de la discussion ---")


def parse_agent_string(agent_str):
    # Exemple : base_agent(Alice) ou agent_codeur("Bob") ou base_agent
    if "(" in agent_str and agent_str.endswith(")"):
        agent_type, param = agent_str.split("(", 1)
        param = param[:-1]  # remove closing )
        param = param.strip("\"'") or None
    else:
        agent_type = agent_str
        param = None

    if agent_type not in AGENT_TYPES:
        raise ValueError(f"Type d'agent inconnu : {agent_type}")

    return AGENT_TYPES[agent_type](name=param)


def main():
    parser = argparse.ArgumentParser(description="Lance une team d'agents avec prompt initial")
    parser.add_argument("prompt", type=str, help="Le sujet de discussion initial")
    parser.add_argument("--agents", nargs="+", required=True, help="Liste des agents (ex: base_agent(Alice) agent_codeur(Bob))")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds de discussion")
    parser.add_argument("--verbose", action="store_true", help="Afficher les messages de debug")
    args = parser.parse_args()

    agents = [parse_agent_string(s) for s in args.agents]
    team = BaseTeam(agents=agents, prompt=args.prompt, n_round=args.n_round, verbose=args.verbose)
    team.run()

if __name__ == "__main__":
    main()
