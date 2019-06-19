from Structured_Code import Team

class Player:
    name = "None"
    team = Team.Team("None")
    age = -1
    overall = -1
    position = "None"

    def __init__(self,name,team,age,overall,position):
        self.name = name
        self.team = team
        self.age = age
        self.overall = overall
        self.position = position

    def __str__(self):
        return self.name