class Team:
    name = "None"
    players = []

    def __init__(self, name,):
        self.name = str(name)
        self.players = []

    def add_player(self, player):
        self.players.append(player)


    def get_avg_overall(self):
        avg=0
        for player in self.players:
            avg+=player.overall
        avg=avg//len(self.players)
        return avg

    def get_avg_age(self):
        avg=0
        for player in self.players:
            avg+=player.age
        avg=avg//len(self.players)
        return avg

    def get_overall_positions(self):
        overalls={"attacker":[],"midfielder":[],"defender":[],"goalkeeper":[]}
        for player in self.players:
            if player.position=="attacker":
                overalls[player.position].append(player.overall)
            elif player.position=="midfielder":
                overalls[player.position].append(player.overall)
            elif player.position=="defender":
                overalls[player.position].append(player.overall)
            elif player.position=="goalkeeper":
                overalls[player.position].append(player.overall)

        for pos in overalls:
            overalls[pos]=sum(overalls[pos])//len(overalls[pos])

        return overalls

    def __str__(self):
        return self.name