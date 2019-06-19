import os
import pandas as pd
import math
from scipy import optimize
import numpy as np
import unidecode
from time import sleep
from MyMethods import *


os.chdir('C:\\Users\\tom_s\\Desktop')  # Set wd
df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="utf-8", sep=";")
match_data = df1  # Save a copy
fifa_data = df2


class Match:
  home_team = 'None'
  away_team = 'None'
  won = -1 # 1 = home team, 0 = out team, 0.5 = draw
  date = ""
  league = ""

  def __init__(self, home_team_name,away_team_name,won,date,league):
      self.home_team = home_team_name
      self.away_team = away_team_name
      self.won = won
      self.date = date
      self.league = league

  def updateTeams(self,home_team,away_team):
      self.home_team=home_team
      self.away_team=away_team

  def __str__(self):
      endstr=""
      if self.won==1:
          endstr=str(self.home_team)+ " won the game."
      elif self.won==0:
          endstr=str(self.away_team)+ " won the game."
      elif self.won==0.5:
          endstr="The game ended in a draw."
      return "The match between "+str(self.home_team)+" and "+str(self.away_team)+" that was being played on "+str(self.date)+". "+endstr


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


def createTeamAndMatchObjects():
    team_coll = []
    match_coll = []
    for i in match_data["Nr"]:
        HomeTeam=match_data["HomeTeam_decoded"][i]
        AwayTeam=match_data["AwayTeam_decoded"][i]
        won=int(match_data["FTHG"][i]>match_data["FTAG"][i])
        if match_data["FTHG"][i]==match_data["FTAG"][i]:
            won=0.5
        date=match_data["Date"][i]
        league = match_data["Div"][i]
        match_list=[HomeTeam,AwayTeam,won,date,league]
        if HomeTeam not in team_coll:
            team_coll.append(HomeTeam)
        if AwayTeam not in team_coll:
            team_coll.append(AwayTeam)
        if match_list not in match_coll:
            match_coll.append(match_list)
    match_coll = transformMatchList(match_coll)
    team_coll=transformTeamList(team_coll)
    return team_coll,match_coll

#for each teamname in list team_coll, replace that element with object Team(teamname)
def transformTeamList(team_coll):
    for i in range(len(team_coll)):
        team_coll[i]=Team(team_coll[i])
    return team_coll

#for each attribute in each element of match_list, replace element with object Match(att[0],att[1],att[2]...)
def transformMatchList(match_coll):
    for i in range(len(match_coll)):
        att=match_coll[i]
        match_coll[i]=Match(att[0],att[1],att[2],att[3],att[4])
    return match_coll

def createPlayerObjects(team_coll):
    player_coll=[]
    for i in fifa_data["Nr"]:
        name=fifa_data["Name"][i]
        team_name=fifa_data["Club"][i]
        age=fifa_data["Age"][i]
        overall=fifa_data["Overall"][i]
        player=Player(name,team_name,age,overall)
        player_coll.append(player)
        team_coll=addPlayerToTeam(team_coll,team_name,player)
    return player_coll

def addPlayerToTeam(team_coll,team_name,player):
    for i in range(len(team_coll)):
        team = team_coll[i]
        if team.name == team_name:
            team.add_player(player)
            team_coll[i] = team
    return team_coll

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

#check collections
def PrintTeamsWith0Players():
    for i in team_coll:
        if len(i.players)==0:
            print(i.__dict__)

def printTotalXvaluesTeams():
    for i in team_coll:
        print(i.__dict__)
        overall = 0
        age = 0
        for j in i.players:
            overall += j.overall
            age += j.age
        print(overall, age)


team_coll,match_coll=createTeamAndMatchObjects()
player_coll=createPlayerObjects(team_coll)
updateTeamsInMatch(match_coll,team_coll)



for game in match_coll:
    if len(game.away_team.players)==0:
        print(game)







# Code linear regression


# def seperate_data(fifa_data,train_factor=0.7):
#     lengte_dataset=len(fifa_data["Nr"])
#     train_size=int(train_factor*lengte_dataset)    #door int() kan er 1 observatie mis worden gelopen
#     test_size=int((1-train_factor)*lengte_dataset)
#
#     fifa_train=fifa_data.head(n=train_size)
#     fifa_test=fifa_data.tail(n=test_size)
#     return fifa_train,fifa_test
#
# fifa_train,fifa_test = seperate_data(fifa_data)





# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors

def total_log_likelihood(coefficients):
    total_log_likelihood = 0
    for match in match_coll:
        log_likelihood=0
        y = match.won
        homeTeam=match.home_team
        awayTeam=match.away_team

        #totale score van team home: overall,age
        x_1_H = 0
        x_2_H = 0

        #tot score van team away
        x_1_A = 0
        x_2_A = 0
        for player in homeTeam.players:
            x_1_H += player.overall
            x_2_H += player.age

        for player in awayTeam.players:
            x_1_A += player.overall
            x_2_A += player.age

        #skip matches without teamplayers (cause=not matching teamnames)
        if x_1_H==0 or x_1_A==0:
            continue

        constante = coefficients[0]
        beta_1 = coefficients[1]
        beta_2 = coefficients[2]
        variance = coefficients[3]


        y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A)
        error = y - y_est
        # printv("error:",error,"variance",variance,"log van..",2 * math.pi * (variance+0.000000001),"gedeeld door..",2 * (variance+0.00000001))
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood = total_log_likelihood + log_likelihood
    print("new model. "+" y_est="+str(y_est)+", y="+str(y)+ "  total log likelihood="+str(total_log_likelihood)+ "  coefficients(constante,beta1,beta2,..)="+str(constante)+",  "+str(beta_1)+",  "+str(beta_2))
    print("    variables:(x1h/x2h)="+str(x_1_H)+", "+str(x_2_H)+"   variables:(x1a/x2a)"+str(x_1_A)+", "+str(x_2_A))


    return total_log_likelihood


# Function log_likelihood berekent de kans van de normale verdeling dat je een
# bepaalde error ziet van 1 observatie
def calc_log_likelihood(error, variance):
    return - (1 / 2) * math.log(2 * math.pi * ((variance+0.000000001)**2) , math.e) - ((error**2)/(2*(variance+0.00000001)**2))
    # return -(1 / 2) * math.log(2 * math.pi * (variance+0.000000001)) - (error ** 2) / (2 * (variance+0.00000001))



# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
coefficient_initialization = [0,0,0,0]
# res = optimize.minimize(total_log_likelihood, coefficient_initialization, method='nelder-mead',
#                options={'xtol': 1e-8, 'disp': True})

# # Nu heb je je beste model
#

# # Nu gaan we waardes voorspellen van test_data
# y = test_data[0]
# x_1 = test_data[1]
# x_2 = test_data[2]
#
# constante = estimated_coefficients[0]
# beta_1 = estimated_coefficients[1]
# beta_2 = estimated_coefficients[2]
# variance = estimated_coefficients[3]
#
# for i in range(len(df[0])):
#     y_est = constante + beta_1 * x_1[i] + beta_2 * x_2[i]
#     error_winst = math.abs(y_est - 1)
#     error_verlies = math.abs(y_est - 0)
#     log_likelihood_winst = log_likelihood(error_winst, variance)
#     log_likelihood_verlies = log_likelihood(error_verlies, variance)
#
#     kans_dat_je_wint_x_maal_groter = log_likelihood_winst / log_likelihood_verlies
#
