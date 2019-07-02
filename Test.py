import Algorithm
import math

#berekenen hoeveel procent van de observaties het model het tegenovergestelde voorspelt  (winnen inplaats van verlizen)
def total_error(coefficients, match_test, algorithm="linear regression"):
    tot_prediction = 0
    tot_error=0
    for match in match_test:
        y = match.won
        homeTeam = match.home_team
        awayTeam = match.away_team
        homeTeamVariables, awayTeamVariables = Algorithm.create_variables(homeTeam, awayTeam, match)
        if algorithm=="linear regression":
            y_est = Algorithm.calc_linear_regression(coefficients, homeTeamVariables, awayTeamVariables)
        elif algorithm=="neural network":
            y_est = Algorithm.calc_neural_network(Algorithm.get_nn_coefficients(coefficients,hiddenlayer_size=3), homeTeamVariables, awayTeamVariables)
        else:
            print("Learn typing you freak")
        correct_prediction=calc_correct_prediction(y_est,y)
        tot_prediction+=correct_prediction**2
        error=error_y_y_est(y_est,y)
        tot_error = tot_error + error**2
    avg_error = "average y-y_est  "+str(tot_error / len(match_test))
    avg_correct_prediction="amount of games predicted right  "+str(1-(tot_prediction/len(match_test)))

    return avg_error,avg_correct_prediction

def calc_correct_prediction(y_est,y):
    error=math.fabs((y_est > 0.5) - y)
    return error

def error_y_y_est(y_est,y):
    error = math.fabs(y - y_est)
    return error

def compete_with_bookmakers(match_test,coefficients,algorithm="linear regression"):
    capital=10000
    for match in match_test:
        homeTeam = match.home_team
        awayTeam = match.away_team
        won=match.won
        homeTeamVariables, awayTeamVariables = Algorithm.create_variables(homeTeam, awayTeam, match)
        constante = coefficients[0]
        variance = coefficients[-1]

        if algorithm=="linear regression":
            y_est = Algorithm.calc_linear_regression(coefficients,homeTeamVariables,awayTeamVariables)
        elif algorithm=="neural network":
            y_est = Algorithm.calc_neural_network(Algorithm.get_nn_coefficients(coefficients,hiddenlayer_size=3),homeTeamVariables,awayTeamVariables)
        else:
            print("Your fingers are too thick to type")

        # nu bereken je de kans dat de error van verliezen voorkomt, en de kans dat de error van winnen voorkomt (gegeven een distribution)
        estimated_odd=get_estimated_winning_odd(y_est,variance)

        official_odd,official_return=get_official_bettingData(match)

        capital=bet(match,capital,estimated_odd,official_odd,official_return,won)

    return capital

def get_estimated_winning_odd(y_est,variance):
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




def manually_testing(algorithm,coefficients,match_coll):
    while True:
        hometeam=input("hometeam: ")
        awayteam=input("awayteam: ")
        match=None
        variable_names_hometeam = {"avg age":None, "avg height":None, "avg weight":None, "attacking rating":None, "midfield rating":None, "defending rating":None,
        "goalkeeper rating":None, "amount of rest days":None}
        variable_names_awayteam = {}
        for i in match_coll:
            if i.home_team.name==hometeam and i.away_team.name==awayteam:
                match=i
                homeTeamVariables,awayTeamVariables=Algorithm.create_variables(match.home_team,match.away_team,match)
                index=0
                for i in variable_names_hometeam:
                    variable_names_hometeam[i]=homeTeamVariables[index]
                    variable_names_awayteam[i]=awayTeamVariables[index]
                    index+=1
                break
        if match==None:
            print("couldn't find a match between "+hometeam+" and "+awayteam)
            len_variables = 8
            homeTeamVariables = []
            awayTeamVariables = []
            print("homeTeamVariables")
            for i in range(len_variables):
                homeTeamVariables.append(int(input("X"+str(i)+" ")))
            print("awayTeamVariables")
            for i in range(len_variables):
                awayTeamVariables.append(int(input("X" + str(i) + " ")))

        variables_input={}
        for i in variable_names_hometeam:
            variables_input[i]=round(variable_names_hometeam[i]-variable_names_awayteam[i],2)


        if algorithm=="neural network":
            y_est = Algorithm.calc_neural_network(Algorithm.get_nn_coefficients(coefficients,3),homeTeamVariables,awayTeamVariables)
        elif algorithm=="linear regression":
            y_est = Algorithm.calc_linear_regression(coefficients,homeTeamVariables,awayTeamVariables)

        estimated_winning_odd=get_estimated_winning_odd(y_est,coefficients[-1])

        print("home team variables are: ",variable_names_hometeam)
        print("away team variables are: ",variable_names_awayteam)
        print("input variables are: ",variables_input)
        print("the output of "+algorithm+" is: ",y_est)
        print("the predicted odd of the hometeam winning is: ",estimated_winning_odd)

