from Structured_Code import Make_Objects
from Structured_Code import Algorithm
from MyMethods import *


def test_data():
    for i in match_coll:
        print("won: ",float(i.won),end="  ")
        printv(i.home_team.name,i.home_team.get_avg_age(),i.home_team.get_overall_positions(),
               "  vs   ",i.away_team.name,i.away_team.get_avg_age(),i.away_team.get_overall_positions())




team_coll=[]
match_coll=[]
player_coll=[]

team_coll,match_coll=Make_Objects.createTeamAndMatchObjects()
player_coll=Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll,team_coll)



model=Algorithm.minimize(match_coll,coefficient_initialization=[0,0,0,0,0,0,0],method='nelder-mead')

