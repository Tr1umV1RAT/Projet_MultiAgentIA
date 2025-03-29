class BaseTeam:
    def __init__(self, name="BaseTeam", project_path="project_outputs", verbose=False):
        self.name = name
        self.project_path = project_path
        self.verbose = verbose

        self.agents = {}
        self.history = []

    def send_message(self, message):
        self.history.append(message)
        if self.verbose:
            print(f"\n🗨️  {message.origine} → {message.destinataire} : {message.contenu}\n")

    def route_message(self, message):
        destinataire = message.destinataire
        if destinataire not in self.agents:
            raise ValueError(f"Agent destinataire inconnu : {destinataire}")
        return self.agents[destinataire].receive_message(message)

    def run_round(self, instruction):
        raise NotImplementedError("Chaque team doit implémenter sa propre méthode run_round().")
