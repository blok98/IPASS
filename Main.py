import os

os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import Algorithm
import Make_Objects
import Saved_Data
import Test
from random import sample


#make list of objects Player,Team,Match
team_coll, match_coll = Make_Objects.createTeamAndMatchObjects()
player_coll = Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll, team_coll)





# TRAINING MODEL

#set bounderies of all coefficients
bounds = [(-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100),
                                      (-100, 100), (-100, 100), (0.1, 50)]

#take random sample of match_data and initialize it to the train data
match_train = sample(match_coll, 500)


opt = {'gtol': 1e-1, 'eps': 100, 'disp': True}

#minimalize the function TOTAL_LOG_LIKELIHOOD with given coefficients. Method is Nelder-Mead which is good for uncertain functions
# model = Algorithm.minimize(match_train, coefficient_initialization=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1],
#                            method="Nelder-Mead", bnds=bounds, options=opt)

model=Saved_Data.open_model()




# TESTING MODEL
#make random sample of data. Initialize this to the test date
match_test = sample(match_coll, 6056)  # sample(match_coll,6056)




#define how much procent the model predicts the right team to win.
avg_err = Test.total_error(list(model.x), match_test)
print(avg_err)


#define the likelihood a team will win given the result of the model
capital=Test.compete_with_bookmakers(match_test,list(model.x))
print(capital)

