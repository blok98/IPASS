import math
import datetime
from scipy import optimize


def create_variables(homeTeam, awayTeam, match):
    # avg score van team home: overall,age
    x1 = homeTeam.get_avg_age()
    x2 = homeTeam.get_avg_height()
    x3 = homeTeam.get_avg_weight()
    x4 = homeTeam.get_avg_positionRating()["attacker"]
    x5 = homeTeam.get_avg_positionRating()["midfielder"]
    x6 = homeTeam.get_avg_positionRating()["defender"]
    x7 = homeTeam.get_avg_positionRating()["goalkeeper"]
    x8 = (match.date-homeTeam.get_last_played_game(match.date)).days
    homeTeamVariables = [x1, x2, x3, x4, x5, x6, x7, x8]
    # tot score van team away
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


def calc_estimated_value(coefficients, homeTeamVariables, awayTeamVariables):
    y_est = coefficients[0]
    # printv("coefficients",coefficients,"homeTeamVariables:",homeTeamVariables,"awayTeamVariables",awayTeamVariables)
    for i in range(1, len(homeTeamVariables) + 1):
        y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))
        # printv("  ",i,"var_hometeam",homeTeamVariables[i-1],"var_awayteam",awayTeamVariables[i-1],"coefficient*varDifference:",coefficients[i],"*",homeTeamVariables[i-1]-awayTeamVariables[i-1],"y_est:",y_est)
    return y_est


# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors
def total_log_likelihood(coefficients, match_coll):
    total_log_likelihood = 0
    tot_error = 0
    for match in match_coll:
        # print(match)
        log_likelihood = 0
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = create_variables(homeTeam, awayTeam, match)

        variance = coefficients[-1]
        # y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A) + beta_3 * (x_3_H - x_3_A)
        y_est = calc_estimated_value(coefficients, homeTeamVariables, awayTeamVariables)
        error = y - y_est
        printerror = math.fabs((y_est > 0.5) - y)   #if y_est is closer to 1, and y=0, than error=1. Vice versa
        tot_error += printerror
        # bereken de likelihood dat een observatie voorkomt
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood = total_log_likelihood + log_likelihood
    avg_error = tot_error / len(match_coll)
    print("totlikelihood", round(total_log_likelihood, 5), end=" ")
    print(avg_error)

    return -total_log_likelihood


# Function log_likelihood berekent de kans van de normale verdeling dat je een
# bepaalde error ziet van 1 observatie
def calc_log_likelihood(error, variance):
    try:
        return -(1 / 2) * math.log(2 * math.pi * (variance+0.001),math.e) - (1 / 2) * ((error+0.001) ** 2) / (variance+0.001)
        # return - (1 / 2) * math.log(2 * math.pi , math.e) - (1/2) * math.log(variance, math.e) - ((error**2)/(2*variance))
    except Exception:
        print(variance,error)
        return -(1 / 2) * math.log(2 * math.pi * (variance + 0.001), math.e) - (1 / 2) * ((error + 0.001) ** 2) / (
                    variance + 0.001)



# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
def minimize(matches, coefficient_initialization=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], method='Nelder-Mead', bnds=[],
             options={'gtol': 1e-3, 'eps': 100, 'disp': True}):
    print("bboouunnddss",bnds)
    model = optimize.minimize(total_log_likelihood, coefficient_initialization, args=(matches), method=method,
                              bounds=bnds, options=options)
    return model


# Nu heb je je beste model


# Nu gaan we waardes voorspellen van test_data
def test_model(coefficients, match_coll):
    for match in match_coll:
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = create_variables(homeTeam, awayTeam, match)
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

        kans_dat_je_wint_x_maal_groter = math.e ** (log_likelihood_winst) / math.e ** (log_likelihood_verlies)
        # printv("ht:", homeTeam, "at", awayTeam, "y:", y, "y_est", y_est, "grotere kans op winnen:",
        #        kans_dat_je_wint_x_maal_groter)


def get_winning_odds(coefficients, match_coll):
    all_odds = []
    for match in match_coll:
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = create_variables(homeTeam, awayTeam, match)
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
        likelihood_winst = math.e ** (log_likelihood_winst)
        likelihood_verlies = math.e ** (log_likelihood_verlies)

        all_odds.append(likelihood_winst / likelihood_verlies)
    return all_odds


#berekenen hoeveel procent van de observaties het model het tegenovergestelde voorspelt  (winnen inplaats van verlizen)
def total_error(coefficients, match_test):
    tot_error = 0
    for match in match_test:
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = create_variables(homeTeam, awayTeam, match)
        y_est = calc_estimated_value(coefficients, homeTeamVariables, awayTeamVariables)
        if y_est > 0.5:
            y_est = 1
        else:
            y_est = 0
        error = math.fabs(y_est - y)
        tot_error = tot_error + error
    avg_error = tot_error / len(match_test)

    return avg_error

