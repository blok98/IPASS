import os


os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import Algorithm
import math
import Make_Objects
import Match
from random import sample


team_coll, match_coll = Make_Objects.createTeamAndMatchObjects()
player_coll = Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll, team_coll)


#
# # TRAINING MODEL
# bounds = [(-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100),
#                                       (-100, 100), (-100, 100), (0.1, 50)]
# match_train = sample(match_coll, 300)
#
#
# opt = {'gtol': 1e-1, 'eps': 100, 'disp': True}
# model = Algorithm.minimize(match_train, coefficient_initialization=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1],
#                            method="Nelder-Mead", bnds=bounds, options=opt)
#
#
#
# # save model in text file
# infile=open("data.txt","w+")
# infile.write(str(model))
#
#
#
# # TESTING MODEL
# match_test = sample(match_coll, 100)  # sample(match_coll,6056)
#
# won = []
# official_returns = [] #hoeveel krijg je ervoor terug
# official_odds = []  #hoveel groter is de kans dat ht wint
# for i in range(len(match_test)):
#     won.append(match_test[i].won)
#     official_return = match_test[i].oddsHomeTeam
#     official_returns.append(official_return)
#     implied_win_probability = 1 / official_return
#     implied_lose_probability = 1 - implied_win_probability
#     official_odds.append(implied_win_probability / implied_lose_probability)
#
# avg_err = Algorithm.total_error(list(model.x), match_test)
# print(avg_err)
#
# estimated_odds = Algorithm.get_winning_odds(list(model.x), match_test)
#
# for i in match_test:
#     print(i.__dict__)
# print(official_returns)
# print(official_odds)
# print(estimated_odds)
#
#
# capital = 10000
# for i in range(len(estimated_odds)):
#     print("estimated odd:",estimated_odds[i])
#     print("official odd:",official_odds[i])
#
#
#     if estimated_odds[i] > 1:
#         print("predict ht will win")
#         if official_odds[i] < estimated_odds[i]:    #if estimated odd is higher than official, expect model is better.
#             print("predict our model is better. Investment made of 100")
#             capital -= 100
#             if won[i] == 1:
#                 capital += official_returns[i] * 100
#                 print("investment won :)")
#             else:
#                 print("investment lost :(")
#     print("capital:",capital,end="\n\n")
#
# print(capital)
