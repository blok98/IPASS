import Team

class Player:
    name = "None"
    team = Team.Team("None")
    age = -1
    height = -1.0
    weight = -1.0
    overall = -1
    position = "None"


    def __init__(self,name,team,age,height,weight,overall,position):
        self.name = name
        self.team = team
        self.age = age
        self.height = height
        self.weight = weight
        self.overall = overall
        self.position = position


    def __str__(self):
        return self.name