import Algorithm
import math

#berekenen hoeveel procent van de observaties het model het tegenovergestelde voorspelt  (winnen inplaats van verlizen)
def total_error(coefficients, match_test):
    tot_error = 0
    for match in match_test:
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = Algorithm.create_variables(homeTeam, awayTeam, match)
        y_est = Algorithm.calc_estimated_value(coefficients, homeTeamVariables, awayTeamVariables)
        if y_est > 0.5:
            y_est = 1
        else:
            y_est = 0
        error = math.fabs(y_est - y)
        tot_error = tot_error + error
    avg_error = tot_error / len(match_test)

    return avg_error


def compete_with_bookmakers(match_test,coefficients):
    capital=10000
    for match in match_test:
        homeTeam = match.home_team
        awayTeam = match.away_team
        won=match.won
        homeTeamVariables, awayTeamVariables = Algorithm.create_variables(homeTeam, awayTeam, match)
        constante = coefficients[0]
        variance = coefficients[-1]

        y_est = constante
        for i in range(1, len(coefficients) - 1):
            y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))

        # nu bereken je de kans dat de error van verliezen voorkomt, en de kans dat de error van winnen voorkomt (gegeven een distribution)
        estimated_odd=get_estimated_winning_odd(match,y_est,variance)

        official_odd,official_return=get_official_bettingData(match)

        capital=bet(match,capital,estimated_odd,official_odd,official_return,won)

    return capital

def get_estimated_winning_odd(match,y_est,variance):
    error_winst = math.fabs(y_est - 1)
    error_verlies = math.fabs(y_est - 0)
    log_likelihood_winst = Algorithm.calc_log_likelihood(error_winst, variance)
    log_likelihood_verlies = Algorithm.calc_log_likelihood(error_verlies, variance)
    likelihood_winst = math.e ** (log_likelihood_winst)
    likelihood_verlies = math.e ** (log_likelihood_verlies)
    estimated_odd = likelihood_winst / likelihood_verlies
    return estimated_odd

def get_official_bettingData(match):
    official_return = match.oddsHomeTeam  # how much more money you get back if you win
    implied_win_probability = 1 / official_return
    implied_lose_probability = 1 - implied_win_probability
    official_odd=(implied_win_probability / implied_lose_probability)   # how much more likely is the hometeam to win
    return official_odd,official_return

def bet(match,capital,estimated_odd,official_odd,official_return,won):

    # Check how much money can be made with the model: If the model predicts a higher change of winning: bet!
    if estimated_odd > 1:
        if official_odd < estimated_odd:  # if estimated odd is higher than official, expect model is better.
            capital -= 100
            if won == 1:
                capital += official_return * 100

    return capital

