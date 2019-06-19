from Structured_Code import Make_Objects
from Structured_Code import Algorithm
from Structured_Code.ClientLineInterface import *
from MyMethods import *

team_coll=[]
match_coll=[]
player_coll=[]

team_coll,match_coll=Make_Objects.createTeamAndMatchObjects()
player_coll=Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll,team_coll)

model=Algorithm.minimize(match_coll,coefficient_initialization=[0,0,0,0,0,0,0],method='nelder-mead')

