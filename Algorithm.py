import math
import datetime
from scipy import optimize
import Saved_Data
import numpy as np
import Test
from matplotlib import pyplot
from time import sleep

global niggahlist
niggahlist = []


# avg score van team home: overall,age
def create_variables(homeTeam, awayTeam, match):
    ''' this creates the variables'''
    x1 = homeTeam.get_avg_age()
    x2 = homeTeam.get_avg_height()
    x3 = homeTeam.get_avg_weight()
    x4 = homeTeam.get_avg_positionRating()["attacker"]
    x5 = homeTeam.get_avg_positionRating()["midfielder"]
    x6 = homeTeam.get_avg_positionRating()["defender"]
    x7 = homeTeam.get_avg_positionRating()["goalkeeper"]
    x8 = (match.date-homeTeam.get_last_played_game(match.date)).days
    homeTeamVariables = [x1, x2, x3, x4, x5, x6, x7, x8]
    x1 = awayTeam.get_avg_age()
    x2 = awayTeam.get_avg_height()
    x3 = awayTeam.get_avg_weight()
    x4 = awayTeam.get_avg_positionRating()["attacker"]
    x5 = awayTeam.get_avg_positionRating()["midfielder"]
    x6 = awayTeam.get_avg_positionRating()["defender"]
    x7 = awayTeam.get_avg_positionRating()["goalkeeper"]
    x8 = (match.date-awayTeam.get_last_played_game(match.date)).days
    awayTeamVariables = [x1, x2, x3, x4, x5, x6, x7, x8]

    return homeTeamVariables, awayTeamVariables


def calc_linear_regression(coefficients, homeTeamVariables, awayTeamVariables):
    y_est = coefficients[0]
    # printv("coefficients",coefficients,"homeTeamVariables:",homeTeamVariables,"awayTeamVariables",awayTeamVariables)
    for i in range(1, len(homeTeamVariables) + 1):
        y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))
        # printv("  ",i,"var_hometeam",homeTeamVariables[i-1],"var_awayteam",awayTeamVariables[i-1],"coefficient*varDifference:",coefficients[i],"*",homeTeamVariables[i-1]-awayTeamVariables[i-1],"y_est:",y_est)
    return y_est

def calc_neural_network(coefficients,homeTeamVariables,awayTeamVariables):
    y_est = coefficients[0]
    coefficients=coefficients[:-1]
    coefficients=coefficients[1:]
    homeTeamVariables=np.asarray(homeTeamVariables)
    awayTeamVariables=np.asarray(awayTeamVariables)
    variables=homeTeamVariables-awayTeamVariables
    var_size=len(variables)
    matrix1=variables
    matrix2=np.asarray(coefficients[:var_size*3]).reshape(3,var_size)
    matrix3=np.asarray(coefficients[-3:])
    y_est += np.dot(np.dot(matrix3,matrix2),matrix1)
    # print("matrixes gemaakt a.h.v. coefficienten:  (coefficienten incl constante and variance=",coefficients)
    # print("matrix1 ",matrix1)
    # print("matrix2 ",matrix2)
    # print("matrix3 ", matrix3)
    return y_est



# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors
def total_log_likelihood(coefficients, match_coll, algorithm="linear regression"):

    total_log_likelihood = 0
    total_correct_predictions=0
    tot_error = 0
    for match in match_coll:
        log_likelihood = 0
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = create_variables(homeTeam, awayTeam, match)

        variance = coefficients[-1]
        # y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A) + beta_3 * (x_3_H - x_3_A)
        if algorithm=="linear regression":
            y_est = calc_linear_regression(coefficients, homeTeamVariables, awayTeamVariables)
        elif algorithm=="neural network":
            y_est = calc_neural_network(coefficients, homeTeamVariables, awayTeamVariables)

        error = math.fabs(y - y_est)
        tot_error+=error
        correct_prediction=Test.calc_correct_prediction(y_est,y)
        total_correct_predictions+=correct_prediction
        # bereken de likelihood dat een observatie voorkomt
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood += log_likelihood


    avg_error = tot_error / len(match_coll)
    niggahlist.append(total_correct_predictions/len(match_coll))
    print("CREATED A NEW MODEL")
    print("totlikelihood", round(total_log_likelihood, 5), end=" ")
    print("the everage y-y_est is: ",avg_error)

    return -total_log_likelihood



# Function log_likelihood berekent de kans van de normale verdeling dat je een
# bepaalde error ziet van 1 observatie
def calc_log_likelihood(error, variance):
    variance = math.fabs(variance)
    try:
        return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (variance)
        # return - (1 / 2) * math.log(2 * math.pi , math.e) - (1/2) * math.log(variance, math.e) - ((error**2)/(2*variance))
    except Exception:
        print(variance,error)
        return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (variance+0.01)



# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
def minimize_model(algorithm, matches, coefficient_initialization=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], method='BFGS',
             options={'maxiter':10000, 'xatol': 0.01, 'fatol': 0.01, 'adaptive': True}, tol=1):

    if algorithm=="neural network":
        coefficient_initialization=get_nn_coefficients(coefficient_initialization,hiddenlayer_size=3)
        coefficient_initialization=[0.52911765,  0.07198612, -0.21088413,  0.3348742 , -0.02000785,
        0.14179519,  0.00728426, -0.10021594,  0.0890723 ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,  0.00659673 ]

    model = optimize.minimize(total_log_likelihood, coefficient_initialization, args=(matches,algorithm), method=method,
                              tol=tol,options=options)

    # save model in text file
    saveIt=input("save model? ")
    if saveIt=="yes" or saveIt=="ja":
        if algorithm=="neural network":
            Saved_Data.save_model_neural_network(model)
        elif algorithm=="linear regression":
            Saved_Data.save_model_linear_regression(model)
    print("model",model)
    return model


def get_nn_coefficients(coefficients,hiddenlayer_size):
    from_variables_to_hidden_layer=coefficients[1:-1]*3
    from_hidden_layer_to_output=[0.1]*hiddenlayer_size
    return [coefficients[0]]+from_variables_to_hidden_layer + from_hidden_layer_to_output+[coefficients[-1]]


def plot_errors(niggahlist=niggahlist):
    index=[]
    for i in range(len(niggahlist)):
        index.append(i)
    return pyplot.scatter(index,niggahlist,1)
