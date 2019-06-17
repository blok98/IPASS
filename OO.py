import os
import pandas as pd
import unidecode
from time import sleep


os.chdir('C:\\Users\\tom_s\\Desktop')  # Set wd
df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="unicode_escape", sep=";")
match_data = df1  # Save a copy
fifa_data = df2




class Match:
  home_team = 'None'
  away_team = 'None'
  won = -1 # 1 = home team, 0 = out team, -1 = draw
  date = ""
  league = ""

  def __init__(self, home_team,away_team,won,date):
      self.home_team = home_team
      self.away_team = away_team
      self.won = won
      self.date = date
      self.league = league


class Team:
    name = "None"
    players = []

    def __init__(self, name,):
        self.name = str(name)
        self.players = []


    def add_player(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players

    def __str__(self):
        return self.name

class Player:
    name = "None"
    team = Team("None")
    age = -1
    overall = -1

    def __init__(self,name,team,age,overall):
        self.name = name
        self.team = team
        self.age = age
        self.overall = overall

    def __str__(self):
        return self.name


player_coll=[]
team_coll=[]
match_coll=[]

for i in match_data["Nr"]:
    HomeTeam=match_data["HomeTeam_decoded"][i]
    AwayTeam=match_data["AwayTeam_decoded"][i]
    won=int(match_data["FTHG"][i]>match_data["FTAG"][i])
    if match_data["FTHG"][i]==match_data["FTAG"][i]:
        won=-1
    date=match_data["Date"][i]
    league = match_data["Div"][i]
    match_list=[HomeTeam,AwayTeam,won,date,league]
    if HomeTeam not in team_coll:
        team_coll.append(HomeTeam)
    if AwayTeam not in team_coll:
        team_coll.append(AwayTeam)
    if match_list not in match_coll:
        match_coll.append(match_list)

#for each teamname in list team_coll, replace that element with object Team(teamname)
for i in range(len(team_coll)):
    team_coll[i]=Team(team_coll[i])

#for each attribute in each element of match_list, replace element with object Match(att[0],att[1],att[2]...)
for i in range(len(match_coll)):
    att=match_coll[i]
    match_coll[i]=Match(att[0],att[1],att[2],att[3])

for i in fifa_data["Nr"]:
    name=fifa_data["Name"][i]
    team_name=fifa_data["Club"][i]
    age=fifa_data["Age"][i]
    overall=fifa_data["Overall"][i]
    player=Player(name,team_name,age,overall)
    player_coll.append(player)
    for i in range(len(team_coll)):
        team=team_coll[i]
        if team.name==team_name:
            team.add_player(player)
            team_coll[i]=team

for i in match_coll:
    if i.home_team=="Manchester City" and i.away_team=="Manchester United":
        print(i.__dict__)


# for i in team_coll:
#     if i.name=="Real Madrid":
#         print(i.__dict__)
#         for j in i.get_players():
#             print(j)






## print all clubs with belonging players
# index=0
# for i in team_coll:
#     print(i)
#     for j in i.get_players():
#         print("  ",j.__dict__)
#     index+=1
# print(str(index)+" resultaten gevonden")

# # simple test
# p1=Player("jan","barcelona",29,94)
# p2=Player("han","city",32,91)
# p3=Player("hendrik","barcelona",22,88)
# p4=Player("piet","city",22,85)
#
# t1=Team("barcelona")
# t1.add_player(p1)
#
# t2=Team("city")
# t2.add_player(p2)
# t2.add_player(p4)
#
# for i in t1.get_players():
#     print(i.__dict__)
#
# for i in t2.get_players():
#     print(i.__dict__)