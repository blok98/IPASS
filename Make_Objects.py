import datetime
import Player,Team,Match
from Calculations import Calculations

class Object_initialisation:
    match_data=None
    fifa_data=None

    player_coll=[]
    team_coll=[]
    match_coll=[]

    def __init__(self,match_dataFrame,fifa_dataFrame):
        self.match_data=match_dataFrame
        self.fifa_data=fifa_dataFrame

    def set_collections(self):
        self.createTeamAndMatchObjects()
        self.createPlayerObjects(self.team_coll)
        self.updateTeamsInMatch(self.match_coll,self.team_coll)


    def createTeamAndMatchObjects(self):
        team_coll = {}
        match_coll = []
        for i in self.match_data["Nr"]:
            HomeTeam = self.match_data["HomeTeam_decoded"][i]
            AwayTeam = self.match_data["AwayTeam_decoded"][i]
            won = int(self.match_data["FTHG"][i] > self.match_data["FTAG"][i])
            if self.match_data["FTHG"][i] == self.match_data["FTAG"][i]:
                won = 0.5
            date = self.match_data["Date"][i]
            date = datetime.datetime.strptime(date, "%d-%m-%Y")
            league = self.match_data["Div"][i]
            oddsHomeTeam = self.match_data["BWH"][i]
            match_list = [HomeTeam, AwayTeam, won, date, league, oddsHomeTeam]
            if HomeTeam not in team_coll:
                team_coll[HomeTeam] = [date]
            else:
                team_coll[HomeTeam].append(date)
            if AwayTeam not in team_coll:
                team_coll[AwayTeam] = [date]
            else:
                team_coll[AwayTeam].append(date)

            if match_list not in match_coll:
                match_coll.append(match_list)
        self.match_coll = self.transformMatchList(match_coll)
        self.team_coll = self.transformTeamList(team_coll)


    # for each teamname in list team_coll, replace that element with object Team(teamname)
    def transformTeamList(self,team_dict):

        team_coll = []
        for i in team_dict:
            dates = team_dict[i]

            team = Team.Team(i)
            team.set_match_dates(dates)
            team_coll.append(team)
        return team_coll

    #for each attribute in each element of match_list, replace element with object Match(att[0],att[1],att[2]...)
    def transformMatchList(self,match_coll):
        for i in range(len(match_coll)):
            att=match_coll[i]
            match_coll[i]=Match.Match(att[0],att[1],att[2],att[3],att[4],att[5])
        return match_coll

    def createPlayerObjects(self,team_coll):
        player_coll = []
        calc=Calculations()
        for i in self.fifa_data["Nr"]:
            name = self.fifa_data["Name"][i]
            team_name = self.fifa_data["Club"][i]
            age = self.fifa_data["Age"][i]
            height = calc.convertHeightToCM(self.fifa_data["Height"][i])
            weight = calc.convertWeightToKG(self.fifa_data["Weight"][i])
            overall = self.fifa_data["Overall"][i]
            position = self.fifa_data["Position"][i]
            position = self.definePosition(position)
            player = Player.Player(name, team_name, age, height, weight, overall, position)
            player_coll.append(player)
            team_coll = self.addPlayerToTeam(team_coll, team_name, player)
        self.player_coll=player_coll

    # first check if team excist in team_coll (and thus also in match_data), than add players to that team.
    def addPlayerToTeam(self,team_coll, team_name, player):
        for i in range(len(team_coll)):
            team = team_coll[i]
            if team.name == team_name:
                team.add_player(player)
                team_coll[i] = team
        self.team_coll=team_coll
        return team_coll

    # convert hometeams and awayteams from match_coll from the type string to the type Team.
    # ... teams that are not present in match_coll will keep their string type
    def updateTeamsInMatch(self,match_coll, team_coll):
        for i in match_coll:

            hometeam = i.home_team
            awayteam = i.away_team
            for j in team_coll:
                if j.name == hometeam:
                    hometeam = j
                if j.name == awayteam:
                    awayteam = j
            i.updateTeams(hometeam, awayteam)

    def definePosition(self,position):
        attacker_positions = "ST", "RS", "LS", "RF", "LW", "RW", "LF", "RF", "CF"
        midfield_positions = "RCM", "LCM", "LDM", "RDM", "CAM", "CDM", "RM", "LM", "LAM", "RAM", "CM"
        defending_positions = "RCB", "LCB", "CB", "RB", "LB", "LWB", "RWB"
        goalkeeper_positions = "GK"
        position = str(position)
        if position in attacker_positions:
            position = "attacker"
        elif position in midfield_positions:
            position = "midfielder"
        elif position in defending_positions:
            position = "defender"
        elif position in goalkeeper_positions:
            position = "goalkeeper"

        return position