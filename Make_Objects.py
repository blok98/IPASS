import pandas as pd
import Calculations
import Match,Team,Player
import datetime

df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="utf-8", sep=";")
match_data = df1  # Save a copy
fifa_data = df2

def createTeamAndMatchObjects():
    team_coll = {}
    match_coll = []
    for i in match_data["Nr"]:
        HomeTeam=match_data["HomeTeam_decoded"][i]
        AwayTeam=match_data["AwayTeam_decoded"][i]
        won=int(match_data["FTHG"][i]>match_data["FTAG"][i])
        if match_data["FTHG"][i]==match_data["FTAG"][i]:
            won=0.5
        date=match_data["Date"][i]
        date=datetime.datetime.strptime(date, "%d-%m-%Y")
        league = match_data["Div"][i]
        oddsHomeTeam=match_data["BWH"][i]
        match_list=[HomeTeam,AwayTeam,won,date,league,oddsHomeTeam]
        if HomeTeam not in team_coll:
            team_coll[HomeTeam]=[date]
        else:
            team_coll[HomeTeam].append(date)
        if AwayTeam not in team_coll:
            team_coll[AwayTeam]=[date]
        else:
            team_coll[AwayTeam].append(date)

        if match_list not in match_coll:
            match_coll.append(match_list)
    match_coll = transformMatchList(match_coll)
    team_coll=transformTeamList(team_coll)
    return team_coll,match_coll

#for each teamname in list team_coll, replace that element with object Team(teamname)
def transformTeamList(team_dict):
    team_coll=[]
    for i in team_dict:
        dates=team_dict[i]
        team=Team.Team(i)
        team.set_match_dates(dates)
        team_coll.append(team)
    return team_coll

#for each attribute in each element of match_list, replace element with object Match(att[0],att[1],att[2]...)
def transformMatchList(match_coll):
    for i in range(len(match_coll)):
        att=match_coll[i]
        match_coll[i]=Match.Match(att[0],att[1],att[2],att[3],att[4],att[5])
    return match_coll



def createPlayerObjects(team_coll):
    player_coll=[]
    for i in fifa_data["Nr"]:
        name=fifa_data["Name"][i]
        team_name=fifa_data["Club"][i]
        age=fifa_data["Age"][i]
        height=Calculations.convertHeightToCM(fifa_data["Height"][i])
        weight=Calculations.convertWeightToKG(fifa_data["Weight"][i])
        overall=fifa_data["Overall"][i]
        position=fifa_data["Position"][i]
        position=definePosition(position)
        player=Player.Player(name,team_name,age,height,weight,overall,position)
        player_coll.append(player)
        team_coll=addPlayerToTeam(team_coll,team_name,player)
    return player_coll

#first check if team excist in team_coll (and thus also in match_data), than add players to that team.
def addPlayerToTeam(team_coll,team_name,player):
    print("team_coll",team_coll)
    for i in range(len(team_coll)):
        team = team_coll[i]
        if team.name == team_name:
            team.add_player(player)
            team_coll[i] = team
    return team_coll

# convert hometeams and awayteams from match_coll from the type string to the type Team.
# ... teams that are not present in match_coll will keep their string type
def updateTeamsInMatch(match_coll,team_coll):
    for i in match_coll:

        hometeam=i.home_team
        awayteam=i.away_team
        for j in team_coll:
            if j.name==hometeam:
                hometeam=j
            if j.name==awayteam:
                awayteam=j
        i.updateTeams(hometeam,awayteam)

def definePosition(position):
    attacker_positions = "ST", "RS", "LS", "RF", "LW", "RW", "LF", "RF", "CF"
    midfield_positions = "RCM", "LCM", "LDM", "RDM", "CAM", "CDM", "RM", "LM", "LAM", "RAM", "CM"
    defending_positions = "RCB", "LCB", "CB", "RB", "LB","LWB","RWB"
    goalkeeper_positions = "GK"
    position=str(position)
    if position in attacker_positions:
        position = "attacker"
    elif position in midfield_positions:
        position = "midfielder"
    elif position in defending_positions:
        position = "defender"
    elif position in goalkeeper_positions:
        position = "goalkeeper"

    return position