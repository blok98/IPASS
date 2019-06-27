import os
import datetime

os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import Algorithm
import math
import Make_Objects
import Match
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
match_train = sample(match_coll, 100)


opt = {'gtol': 1e-1, 'eps': 100, 'disp': True}

#minimalize the function TOTAL_LOG_LIKELIHOOD with given coefficients. Method is Nelder-Mead which is good for uncertain functions
model = Algorithm.minimize(match_train, coefficient_initialization=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1],
                           method="Nelder-Mead", bnds=bounds, options=opt)
print(model)

# save model in text file
infile=open("data.txt","w+")
infile.write(str(model))


# TESTING MODEL
#make random sample of data. Initialize this to the test date
match_test = sample(match_coll, 6056)  # sample(match_coll,6056)


won = []
official_returns = [] #how much more money you get back if you win
official_odds = []  #how much more likely is the hometeam to win
#Now make the lists official returns and official odds. For every match take the odds and the result(0,1), and convert it correctly
for i in range(len(match_test)):
    won.append(match_test[i].won)
    official_return = match_test[i].oddsHomeTeam
    official_returns.append(official_return)
    implied_win_probability = 1 / official_return
    implied_lose_probability = 1 - implied_win_probability
    official_odds.append(implied_win_probability / implied_lose_probability)

#define how much procent the model predicts the right team to win.
avg_err = Algorithm.total_error(list(model.x), match_test)
print(avg_err)

#define the likelihood a team will win given the result of the model
estimated_odds = Algorithm.get_winning_odds(list(model.x), match_test)
print(estimated_odds)

#Check how much money can be made with the model: If the model predicts a higher change of winning: bet!
capital = 10000
for i in range(len(estimated_odds)):

    if estimated_odds[i] > 1:
        if official_odds[i] < estimated_odds[i]:    #if estimated odd is higher than official, expect model is better.
            capital -= 100
            if won[i] == 1:
                capital += official_returns[i] * 100

print(capital)
