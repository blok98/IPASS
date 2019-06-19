from Structured_Code import Make_Objects
from Structured_Code import Algorithm
from Structured_Code import ClientLineInterface
from MyMethods import *

team_coll,match_coll=Make_Objects.createTeamAndMatchObjects()
player_coll=Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll,team_coll)

optimalCoefficients=[0.39487332	,-0.30308159,0.0708144,-0.01632515,-0.06523987,0.01900337,0.51511925]

model=Algorithm.minimize(match_coll,coefficient_initialization=[0,0,0,0,0,0,0],method='nelder-mead')

# Algorithm.test_model(optimalCoefficients,match_coll)


