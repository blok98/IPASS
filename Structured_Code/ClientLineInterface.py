from MyMethods import *

def test_data(match_coll):
    for i in match_coll:
        print("won: ",float(i.won),end="  ")
        printv(i.home_team.name,i.home_team.get_avg_age(),i.home_team.get_overall_positions(),
               "  vs   ",i.away_team.name,i.away_team.get_avg_age(),i.away_team.get_overall_positions())

def print_proces(y_est,y,total_log_likelihood,coefficients,homeTeamVariables,awayTeamVariables):
    print("new model. "+" y_est="+str(y_est)+", y="+str(y)+ "  total log likelihood="+str(total_log_likelihood)+ "  coefficients(constante,beta1,beta2,..)=",coefficients)
    printv("    hometeam: ",homeTeamVariables,"  awayteam: ",awayTeamVariables)