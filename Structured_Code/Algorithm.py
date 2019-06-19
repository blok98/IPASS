import math
from scipy import optimize
from MyMethods import *


# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors
def total_log_likelihood(coefficients,match_coll):
    total_log_likelihood = 0
    for match in match_coll:
        log_likelihood=0
        y = match.won
        homeTeam=match.home_team
        awayTeam=match.away_team

        #avg score van team home: overall,age
        x1 = homeTeam.get_avg_age()
        x2 = homeTeam.get_overall_positions()["attacker"]
        x3 = homeTeam.get_overall_positions()["midfielder"]
        x4 = homeTeam.get_overall_positions()["defender"]
        x5 = homeTeam.get_overall_positions()["goalkeeper"]
        homeTeamVariables=[x1,x2,x3,x4,x5]

        #tot score van team away
        x1 = awayTeam.get_avg_age()
        x2 = awayTeam.get_overall_positions()["attacker"]
        x3 = awayTeam.get_overall_positions()["midfielder"]
        x4 = awayTeam.get_overall_positions()["defender"]
        x5 = awayTeam.get_overall_positions()["goalkeeper"]
        awayTeamVariables=[x1,x2,x3,x4,x5]

        constante = coefficients[0]
        variance = coefficients[-1]

        # y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A) + beta_3 * (x_3_H - x_3_A)
        y_est=constante
        for i in range(1,len(coefficients)-1):
            y_est += (coefficients[i]*(homeTeamVariables[i-1]-awayTeamVariables[i-1]))

        error = y - y_est
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood = total_log_likelihood + log_likelihood
        game=match
    print("new model. "+" y_est="+str(y_est)+", y="+str(y)+ "  total log likelihood="+str(total_log_likelihood)+ "  coefficients(constante,beta1,beta2,..)=",coefficients)
    printv("    hometeam: ",homeTeamVariables,"  awayteam: ",awayTeamVariables)

    return -1*total_log_likelihood


# Function log_likelihood berekent de kans van de normale verdeling dat je een
# bepaalde error ziet van 1 observatie
def calc_log_likelihood(error, variance):
    return - (1 / 2) * math.log(2 * math.pi * ((variance+0.000000001)**2) , math.e) - ((error**2)/(2*(variance+0.00000001)**2))
    # return -(1 / 2) * math.log(2 * math.pi * (variance+0.000000001)) - (error ** 2) / (2 * (variance+0.00000001))


# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
def minimize(matches,coefficient_initialization=[0,0,0,0,0,0,0],method='nelder-mead'):
    model = optimize.minimize(total_log_likelihood, coefficient_initialization, args=(matches), method=method,
               options={'xtol': 1e-8, 'disp': True})
    return model







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
