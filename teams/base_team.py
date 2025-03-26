import argparse
from skills.communication.messages import Message
from skills.communication.communication import Communication
from agents.base_agent import BaseAgent
from roles.base_role import BaseRole

class BaseTeam:
    def __init__(self, nom_team: str, agents, n_rounds: int = 5, prompt_initial: str = None, verbose: bool = False):
        self.nom_team = nom_team
        self.prompt_initial = prompt_initial
        self.n_rounds = n_rounds
        self.verbose = verbose

        # Gestion flexible des agents (liste ou dictionnaire)
        if isinstance(agents, dict):
            self.agents_dict = agents
        else:
            self.agents_dict = {agent.name: agent for agent in agents}

        self.agents = list(self.agents_dict.values())

        # Communication centrale
        self.communication = Communication(verbose=self.verbose)

        # Injecter la communication centralisée dans chaque agent
        for agent in self.agents:
            agent.communication = self.communication
            agent.communication.set_route_callback(self.route_message)

        if self.verbose:
            print(f"[Init] Team '{self.nom_team}' initialisée avec agents : {', '.join(self.agents_dict)}")

    def route_message(self, message: Message):
        """Route les messages aux agents selon le destinataire spécifié."""
        dest = message.destinataire

        # Envoi à tous les agents si destinataire non spécifié ou 'ALL'
        if not dest or dest.lower() in {"all", "tous"}:
            destinataires = self.agents
        else:
            destinataires = [self.agents_dict[dest]] if dest in self.agents_dict else []

        for agent in destinataires:
            agent.receive_message(message)

    def envoyer_prompt_initial(self):
        if self.prompt_initial:
            message_initial = Message(
                origine="System",
                destinataire="ALL",
                type_message="system",
                contenu=self.prompt_initial,
                memoriser=False
            )
            self.communication.send(message_initial)
            if self.verbose:
                print(f"[Team '{self.nom_team}'] Prompt initial envoyé : {self.prompt_initial}")

    def run(self):
        self.envoyer_prompt_initial()

        for tour in range(1, self.n_rounds + 1):
            if self.verbose:
                print(f"\n--- Tour {tour}/{self.n_rounds} ---")

            for agent in self.agents:
                agent.process_messages()

        if self.verbose:
            print("\n[Team] Fin des interactions")

    def step(self):
        for agent in self.agents:
            agent.process_messages()

# --- Interface CLI directe ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une conversation autonome entre agents.")
    parser.add_argument("--agents", nargs='+', required=True, help="Noms des agents participants")
    parser.add_argument("prompt", type=str, help="Prompt initial pour démarrer la conversation")
    parser.add_argument("--n_rounds", type=int, default=5, help="Nombre de tours d'interaction")
    parser.add_argument("--verbose", action="store_true", help="Active les messages détaillés")

    args = parser.parse_args()

    # Création automatique des agents à partir des noms fournis
    agents_instances = {}
    for agent_name in args.agents:
        role = BaseRole(name=f"Role_{agent_name}", objectif="Participer à une conversation autonome")
        agent = BaseAgent(name=agent_name, role=role, verbose=args.verbose)
        agents_instances[agent_name] = agent

    team = BaseTeam(
        nom_team="Autonome",
        agents=agents_instances,
        n_rounds=args.n_rounds,
        prompt_initial=args.prompt,
        verbose=args.verbose
    )

    team.run()