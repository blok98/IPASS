import os

os.chdir("C:\\Users\\tom_s\\Desktop\\IPASS\\Python")

import Algorithm
import Make_Objects
import Saved_Data
import Test
import Calculations
from random import sample
from matplotlib import pyplot


#make list of objects Player,Team,Match
team_coll, match_coll = Make_Objects.createTeamAndMatchObjects()
player_coll = Make_Objects.createPlayerObjects(team_coll)
Make_Objects.updateTeamsInMatch(match_coll, team_coll)

algorithm="neural network"

while True:
    match_train,match_test=match_coll[:50],match_coll[:50]
    process=input("Use saved model? (Model="+algorithm+") ")
    if process=="yes" or process=="ja":
        if algorithm=="neural network":
            model = Saved_Data.open_model_neural_network()
        elif algorithm=="linear regression":
            model = Saved_Data.open_model_linear_regression()
        # match_train,match_test=Saved_Data.open_datasets()
        print(model)
        break
    else:
        process=input("Are you sure you want to train the data? (Algorithm="+algorithm+") ")
        if process=="yes" or process=="ja":
            # match_train, match_test = Calculations.seperateData(match_coll, train=0.7, test=0.3)
            # match_train, match_test = sample(match_coll, 50) , sample(match_coll, 6056)
            # Saved_Data.save_datasets(match_train,match_test)

            # set bounderies of all coefficients
            bounds = [(-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100),
                      (-100, 100), (-100, 100), (0.15, 50)]

            opt = {'gtol': 1e-1, 'eps': 100, 'disp': True}

            # minimalize the function TOTAL_LOG_LIKELIHOOD with given coefficients. Method is Nelder-Mead which is good for uncertain functions
            model = Algorithm.minimize_model(algorithm, match_train, coefficient_initialization=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1],
                                       method="Nelder-Mead", bnds=bounds, options=opt)
            print(model)
            break


Algorithm.plot_errors()

#define how much procent the model predicts the right team to win.
avg_err,avg_correct_prediction = Test.total_error(list(model.x), match_test, algorithm=algorithm)
print(avg_err,avg_correct_prediction)


#define the likelihood a team will win given the result of the model
capital=Test.compete_with_bookmakers(match_test, list(model.x), algorithm=algorithm)
print(capital)


Test.manually_testing(algorithm,list(model.x),match_coll)

