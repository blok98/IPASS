class Team:
    name = "None"
    players = []
    matchDates=[]

    def __init__(self, name,):
        self.name = str(name)
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def set_match_dates(self,list_dates):
        list_dates.sort()
        self.matchDates=list_dates

    def get_last_played_game(self,date):
        dateLastPlayed=self.matchDates[self.matchDates.index(date)-1]
        return dateLastPlayed

    def get_avg_age(self):
        avg=0
        for player in self.players:
            avg+=player.age
        avg=avg//len(self.players)
        return avg

    def get_avg_overall(self):
        avg=0
        for player in self.players:
            avg+=player.overall
        avg=avg//len(self.players)
        return avg

    def get_avg_height(self):
        avg=0
        players_without_stats=0
        for player in self.players:
            avg += player.height
            if player.height==0.0:
                players_without_stats+=1
        avg = avg / (len(self.players)-players_without_stats)
        return round(avg,2)

    def get_avg_weight(self):
        avg=0
        players_without_stats=0
        for player in self.players:
            avg += player.weight
            if player.weight==0.0:
                players_without_stats+=1
        avg = avg / (len(self.players)-players_without_stats)
        return round(avg,2)

    def get_avg_positionRating(self):
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