# Code linear regression
import os
import pandas as pd
import scipy

# Set the working directory and read all 6 years data files
os.chdir('C:\\Users\\tom_s\\Desktop')  # Set wd
df1 = pd.read_csv("All_data.csv", index_col=False, encoding="unicode_escape", sep=";")
df2 = pd.read_csv("Fifa_data.csv", index_col=False, encoding="unicode_escape", sep=";")
match_data = df1  # Save a copy
fifa_data = df2


def seperate_data(fifa_data,train_factor=0.7):
    lengte_dataset=len(fifa_data["Nr"])
    train_size=int(train_factor*lengte_dataset)    #door int() kan er 1 observatie mis worden gelopen
    test_size=int((1-train_factor)*lengte_dataset)

    fifa_train=fifa_data.head(n=train_size)
    fifa_test=fifa_data.tail(n=test_size)
    return fifa_train,fifa_test

fifa_train,fifa_test = seperate_data(fifa_data)




#
# # Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
# # van alle log_likelihoods van alle errors
# def total_log_likelihood(coefficients):
#     total_log_likelihood = 0
#
#     y = fifa_data[0]
#     x_1 = train_data[1]
#     x_2 = train_data[2]
#
#     constante = coefficients[0]
#     beta_1 = coefficients[1]
#     beta_2 = coefficients[2]
#     variance = coefficients[3]
#
#     for i in range(len(df[0])):
#         y_est = constante + beta_1 * x_1[i] + beta_2 * x_2[i]
#         error = y - y_est
#         log_likelihood = log_likelihood(error, variance)
#         total_log_likelihood = total_log_likelihood + log_likelihood
#
#     return (total_log_likelihood)
#
#
# # Function log_likelihood berekent de kans van de normale verdeling dat je een
# # bepaalde error ziet van 1 observatie
# def log_likelihood(error, variance):
#     return (-(1 / 2) * log(2 * math.pi * variance) - (error ^ 2) / (2 * variance))
#
#
# # Minimaliseer je total_log_likelihood (of maximaliseer de kans dat je de
# # gegeven errors ziet) door je coefficients te veranderen en
# # sla de coefficients op die de laagste total_log_likelihood hebben
# coefficient_initialization = [0, 0, 0, 0]
# res = minimize(total_log_likelihood, coefficient_initialization, method='nelder-mead',
#                options={'xtol': 1e-8, 'disp': True})
#
# # Nu heb je je beste model
#
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