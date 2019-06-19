import math
from scipy import optimize
from Structured_Code.ClientLineInterface import *
from MyMethods import *

def create_variables(homeTeam,awayTeam):
    # avg score van team home: overall,age
    x1 = homeTeam.get_avg_age()
    x2 = homeTeam.get_overall_positions()["attacker"]
    x3 = homeTeam.get_overall_positions()["midfielder"]
    x4 = homeTeam.get_overall_positions()["defender"]
    x5 = homeTeam.get_overall_positions()["goalkeeper"]
    homeTeamVariables = [x1, x2, x3, x4, x5]

    # tot score van team away
    x1 = awayTeam.get_avg_age()
    x2 = awayTeam.get_overall_positions()["attacker"]
    x3 = awayTeam.get_overall_positions()["midfielder"]
    x4 = awayTeam.get_overall_positions()["defender"]
    x5 = awayTeam.get_overall_positions()["goalkeeper"]
    awayTeamVariables = [x1, x2, x3, x4, x5]

    return homeTeamVariables,awayTeamVariables


# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors
def total_log_likelihood(coefficients,match_coll):
    total_log_likelihood = 0
    for match in match_coll:
        log_likelihood=0
        y = match.won
        homeTeam=match.home_team
        awayTeam=match.away_team
        homeTeamVariables,awayTeamVariables=create_variables(homeTeam,awayTeam)
        constante = coefficients[0]
        variance = coefficients[-1]

        # y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A) + beta_3 * (x_3_H - x_3_A)
        y_est=constante
        for i in range(1,len(coefficients)-1):
            y_est += (coefficients[i]*(homeTeamVariables[i-1]-awayTeamVariables[i-1]))

        error = y - y_est
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood = total_log_likelihood + log_likelihood

    print_proces(y_est,y,total_log_likelihood,coefficients,homeTeamVariables,awayTeamVariables)

    return total_log_likelihood


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
    return coefficient_initialization







# Nu heb je je beste model


# Nu gaan we waardes voorspellen van test_data
def test_model(coefficients,match_coll):

    for match in match_coll:
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables,awayTeamVariables=create_variables(homeTeam,awayTeam)
        constante = coefficients[0]
        variance = coefficients[-1]

        y_est = constante
        for i in range(1, len(coefficients) - 1):
            y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))

        # nu bereken je de kans dat de error van verliezen voorkomt, en de kans dat de error van winnen voorkomt (gegeven een distribution)
        error_winst = math.fabs(y_est - 1)
        error_verlies = math.fabs(y_est - 0)
        log_likelihood_winst = calc_log_likelihood(error_winst, variance)
        log_likelihood_verlies = calc_log_likelihood(error_verlies, variance)

        kans_dat_je_wint_x_maal_groter = log_likelihood_winst / log_likelihood_verlies
        printv("ht:",homeTeam,"at",awayTeam,"y:",y,"y_est",y_est,"grotere kans op winnen:",kans_dat_je_wint_x_maal_groter)
