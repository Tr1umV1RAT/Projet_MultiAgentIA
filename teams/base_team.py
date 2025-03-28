import argparse
import os
import sys
import json
import uuid
from datetime import datetime
from agents.base_agent import BaseAgent
from skills.communication.messages import Message

AGENT_TYPES = {
    "base_agent": BaseAgent,
}

class BaseTeam:
    def __init__(self, agents, prompt, n_round=5, verbose=False, project_name=None, load_path=None):
        self.agents = agents
        self.initial_prompt = prompt
        self.n_round = n_round
        self.verbose = verbose
        self.history = []

        if load_path:
            self.project_path = load_path
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = project_name or f"project_{timestamp}"
            self.project_path = os.path.join("projects", name)
            os.makedirs(self.project_path, exist_ok=True)

    def run(self):
        conversation_id = "team_convo"

        if not self.history:
            if self.verbose:
                print("\n--- Début de la conversation ---\n")
            system_message = Message(
                origine="système",
                destinataire="tous",
                contenu=self.initial_prompt,
                conversation_id=conversation_id
            )
            self.history.append(system_message)
            for agent in self.agents:
                agent.receive_message(system_message)

        for r in range(1, self.n_round + 1):
            if self.verbose:
                print(f"\n--- Round {r} ---")

            new_messages = []
            for agent in self.agents:
                last_message = self.history[-1]
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
            self.save_state()

        if self.verbose:
            print("\n--- Fin de la discussion ---")

    def save_state(self):
        history_path = os.path.join(self.project_path, "history.json")
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump([msg.to_dict() for msg in self.history], f, indent=2)

        config = {
            "agents": [
                {
                    "name": agent.name,
                    "type": agent.__class__.__name__,
                } for agent in self.agents
            ],
            "prompt": self.initial_prompt,
            "n_round": self.n_round,
        }
        config_path = os.path.join(self.project_path, "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def load_from_path(cls, path, append_prompt=None, verbose=False):
        with open(os.path.join(path, "config.json"), encoding="utf-8") as f:
            config = json.load(f)

        with open(os.path.join(path, "history.json"), encoding="utf-8") as f:
            raw_history = json.load(f)
            history = [Message.from_dict(m) for m in raw_history]

        agents = [BaseAgent.from_config(a, verbose=verbose) for a in config["agents"]]
        team = cls(
            agents=agents,
            prompt=config["prompt"],
            n_round=config["n_round"],
            verbose=verbose,
            project_name=os.path.basename(path),
            load_path=path
        )
        team.history = history

        if append_prompt:
            msg = Message(
                origine="système",
                destinataire="tous",
                contenu=append_prompt,
                conversation_id="team_convo"
            )
            team.history.append(msg)
            for agent in team.agents:
                agent.receive_message(msg)

        return team


def parse_agent_string(agent_str):
    if "(" in agent_str and agent_str.endswith(")"):
        agent_type, param = agent_str.split("(", 1)
        param = param[:-1].strip("\"'") or None
    else:
        agent_type = agent_str
        param = None

    if agent_type not in AGENT_TYPES:
        raise ValueError(f"Type d'agent inconnu : {agent_type}")

    return AGENT_TYPES[agent_type](name=param)


def main():
    parser = argparse.ArgumentParser(description="Lance ou charge une team d'agents avec prompt initial")
    parser.add_argument("prompt", type=str, nargs="?", help="Le sujet de discussion initial")
    parser.add_argument("--agents", nargs="+", help="Liste des agents (ex: base_agent(Alice) base_agent)")
    parser.add_argument("--n_round", type=int, default=5, help="Nombre de rounds de discussion")
    parser.add_argument("--verbose", action="store_true", help="Afficher les messages de debug")
    parser.add_argument("--project_name", type=str, help="Nom du projet ")
    parser.add_argument("--load", type=str, help="Chemin vers un projet à recharger")
    parser.add_argument("--append", type=str, help="Nouveau prompt à injecter avant de reprendre")
    args = parser.parse_args()

    if args.load:
        team = BaseTeam.load_from_path(args.load, append_prompt=args.append, verbose=args.verbose)
    else:
        if not args.prompt or not args.agents:
            print("Si vous ne chargez pas un projet, vous devez fournir un prompt et des agents.")
            sys.exit(1)
        agents = [parse_agent_string(s) for s in args.agents]
        team = BaseTeam(
            agents=agents,
            prompt=args.prompt,
            n_round=args.n_round,
            verbose=args.verbose,
            project_name=args.project_name
        )

    team.run()

if __name__ == "__main__":
    main()
