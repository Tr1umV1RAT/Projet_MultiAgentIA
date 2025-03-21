from teams.base_team import BaseTeam

class DebatTeam(BaseTeam):
    def __init__(self, agents, rounds=3):
        super().__init__(agents, rounds)
