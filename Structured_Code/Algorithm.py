import math
from scipy import optimize


# Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# van alle log_likelihoods van alle errors
def total_log_likelihood(coefficients,match_coll):
    total_log_likelihood = 0
    for match in match_coll:
        log_likelihood=0
        y = match.won
        homeTeam=match.home_team
        awayTeam=match.away_team

        #totale score van team home: overall,age
        x_1_H = 0
        x_2_H = 0

        #tot score van team away
        x_1_A = 0
        x_2_A = 0
        for player in homeTeam.players:
            x_1_H += player.overall
            x_2_H += player.age

        for player in awayTeam.players:
            x_1_A += player.overall
            x_2_A += player.age

        #skip matches without teamplayers (cause=not matching teamnames)
        if x_1_H==0 or x_1_A==0:
            continue

        constante = coefficients[0]
        beta_1 = coefficients[1]
        beta_2 = coefficients[2]
        variance = coefficients[3]


        y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A)
        error = y - y_est
        log_likelihood = calc_log_likelihood(error, variance)
        total_log_likelihood = total_log_likelihood + log_likelihood

    print("new model. "+" y_est="+str(y_est)+", y="+str(y)+ "  total log likelihood="+str(total_log_likelihood)+ "  coefficients(constante,beta1,beta2,..)="+str(constante)+"   "+str(beta_1)+"   "+str(beta_2))
    print("    variables:(x1h/x2h)="+str(x_1_H)+", "+str(x_2_H)+"   variables:(x1a/x2a)"+str(x_1_A)+", "+str(x_2_A))


    return total_log_likelihood


# Function log_likelihood berekent de kans van de normale verdeling dat je een
# bepaalde error ziet van 1 observatie
def calc_log_likelihood(error, variance):
    return - (1 / 2) * math.log(2 * math.pi * ((variance+0.000000001)**2) , math.e) - ((error**2)/(2*(variance+0.00000001)**2))
    # return -(1 / 2) * math.log(2 * math.pi * (variance+0.000000001)) - (error ** 2) / (2 * (variance+0.00000001))



# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
def minimize(matches,coefficient_initialization=[0,0,0,0],method='nelder-mead'):
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
