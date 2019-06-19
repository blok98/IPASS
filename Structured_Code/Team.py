class Team:
    name = "None"
    players = []

    def __init__(self, name,):
        self.name = str(name)
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def __str__(self):
        return self.name