import math
from scipy import optimize
import numpy as np
import pickle
from matplotlib import pyplot

class Algorithm:
    method='Nelder-Mead'
    opt = {'maxiter': 10000, 'xatol': 0.1, 'fatol': 0.01, 'adaptive': True}
    model = None
    avg_error_timeline=[]


    def __init__(self):
        pass

    # avg score van team home: overall,age
    def create_variables(self,homeTeam, awayTeam, match):
        ''' this creates the variables'''
        x1 = homeTeam.get_avg_age()
        x2 = homeTeam.get_avg_height()
        x3 = homeTeam.get_avg_weight()
        x4 = homeTeam.get_avg_positionRating()["attacker"]
        x5 = homeTeam.get_avg_positionRating()["midfielder"]
        x6 = homeTeam.get_avg_positionRating()["defender"]
        x7 = homeTeam.get_avg_positionRating()["goalkeeper"]
        x8 = (match.date - homeTeam.get_last_played_game(match.date)).days
        homeTeamVariables = [x1, x2, x3, x4, x5, x6, x7, x8]
        x1 = awayTeam.get_avg_age()
        x2 = awayTeam.get_avg_height()
        x3 = awayTeam.get_avg_weight()
        x4 = awayTeam.get_avg_positionRating()["attacker"]
        x5 = awayTeam.get_avg_positionRating()["midfielder"]
        x6 = awayTeam.get_avg_positionRating()["defender"]
        x7 = awayTeam.get_avg_positionRating()["goalkeeper"]
        x8 = (match.date - awayTeam.get_last_played_game(match.date)).days
        awayTeamVariables = [x1, x2, x3, x4, x5, x6, x7, x8]

        return homeTeamVariables, awayTeamVariables



    # Function log_likelihood berekent de kans van de normale verdeling dat je een
    # bepaalde error ziet van 1 observatie
    def calc_log_likelihood(self,error, variance):
        try:
            return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (variance)
            # return - (1 / 2) * math.log(2 * math.pi , math.e) - (1/2) * math.log(variance, math.e) - ((error**2)/(2*variance))
        except Exception:
            print(variance, error)
            return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (
                    variance + 0.001)

    def save(self, name):
        with open(name+".pickle", "wb") as f:
            pickle.dump(self, f)

    def load(self,name):
        with open(name+".pickle", "rb") as f:
            newObj = pickle.load(f)
            self.__dict__.update(newObj.__dict__)

    def plot_errors(self):
        x_values=[]
        y_values=self.avg_error_timeline
        for i in range(len(y_values)):
            x_values.append(i)
        pyplot.scatter(x_values,y_values,5)
        pyplot.show()







class Neural_network(Algorithm):
    match_train=[]
    coefficients=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1]
    tol = 1000000

    def __init__(self,match_train):
        self.match_train=match_train
        self.coefficients=self.get_nn_coefficients(3)

    def get_nn_coefficients(self,hiddenlayer_size):
        from_variables_to_hidden_layer = self.coefficients[1:-1] * 3
        from_hidden_layer_to_output = [0.1] * hiddenlayer_size
        return [self.coefficients[0]] + from_variables_to_hidden_layer + from_hidden_layer_to_output + [self.coefficients[-1]]

    def calc_neural_network(self, homeTeamVariables, awayTeamVariables):
        coefficients=self.coefficients
        y_est = coefficients[0]
        coefficients = coefficients[:-1]
        homeTeamVariables = np.asarray(homeTeamVariables)
        awayTeamVariables = np.asarray(awayTeamVariables)
        variables = homeTeamVariables - awayTeamVariables
        var_size = len(variables)
        matrix1 = variables
        matrix2 = np.asarray(coefficients[:var_size * 3]).reshape(3, var_size)
        matrix3 = np.asarray(coefficients[-3:])
        y_est += np.dot(np.dot(matrix3, matrix2), matrix1)
        return y_est


    def minimize_model(self):
        self.avg_error_timeline=[]
        coefficient_initialization = self.coefficients

        model = optimize.minimize(self.total_log_likelihood, coefficient_initialization, args=(self.match_train),
                                  method=self.method,options=self.opt,tol=self.tol)
        self.model=model
        print(model)

        # save model in text file
        # saveIt = input("save model? ")
        # if saveIt == "yes" or saveIt == "ja":
        #     if algorithm == "neural network":
        #         Saved_Data.save_model_neural_network(model)
        #     elif algorithm == "linear regression":
        #         Saved_Data.save_model_linear_regression(model)
        # print("model", model)
        # return model

        # Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
        # van alle log_likelihoods van alle errors




    def total_log_likelihood(self, coefficients, match_test):
        total_log_likelihood = 0
        total_correct_predictions = 0
        tot_error = 0
        for match in match_test:
            log_likelihood = 0
            y = match.won
            homeTeam = match.home_team
            awayTeam = match.away_team
            homeTeamVariables, awayTeamVariables = self.create_variables(homeTeam, awayTeam, match)

            variance = coefficients[-1]

            y_est = self.calc_neural_network(homeTeamVariables,awayTeamVariables)

            error = y - y_est
            log_likelihood = self.calc_log_likelihood(error, variance)
            total_log_likelihood = total_log_likelihood + log_likelihood

            tot_error += error


        avg_error = tot_error / len(match_test)
        self.avg_error_timeline.append(avg_error)

        print("totlikelihood", round(total_log_likelihood, 5), end=" ")
        print(avg_error)

        return -total_log_likelihood







class Linear_regression(Algorithm):
    match_train=[]
    coefficients=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1]
    tol = 1000

    def __init__(self,match_train):
        self.match_train=match_train


    def calc_linear_regression(self,coefficients, homeTeamVariables, awayTeamVariables):
        y_est = coefficients[0]
        # printv("coefficients",coefficients,"homeTeamVariables:",homeTeamVariables,"awayTeamVariables",awayTeamVariables)
        for i in range(1, len(homeTeamVariables) + 1):
            y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))
            # printv("  ",i,"var_hometeam",homeTeamVariables[i-1],"var_awayteam",awayTeamVariables[i-1],"coefficient*varDifference:",coefficients[i],"*",homeTeamVariables[i-1]-awayTeamVariables[i-1],"y_est:",y_est)
        return y_est


    def minimize_model(self):
        self.avg_error_timeline=[]
        coefficient_initialization = self.coefficients

        model = optimize.minimize(self.total_log_likelihood, coefficient_initialization, args=(self.match_train),
                                  method=self.method,options=self.opt,tol=self.tol)
        self.model = model

        print(model)

        # save model in text file
        # saveIt = input("save model? ")
        # if saveIt == "yes" or saveIt == "ja":
        #     if algorithm == "neural network":
        #         Saved_Data.save_model_neural_network(model)
        #     elif algorithm == "linear regression":
        #         Saved_Data.save_model_linear_regression(model)
        # print("model", model)
        # return model

        # Function total_log_likelihood berekent eerst alle errors zelf en daarna de som
        # van alle log_likelihoods van alle errors


    def total_log_likelihood(self, coefficients, match_train):
        total_log_likelihood = 0
        total_correct_predictions = 0
        tot_error = 0
        for match in match_train:
            log_likelihood = 0
            y = match.won
            homeTeam = match.home_team
            awayTeam = match.away_team
            homeTeamVariables, awayTeamVariables = self.create_variables(homeTeam, awayTeam, match)

            variance = coefficients[-1]
            # y_est = constante + beta_1 * (x_1_H - x_1_A) + beta_2 * (x_2_H - x_2_A) + beta_3 * (x_3_H - x_3_A)

            y_est = self.calc_linear_regression(coefficients, homeTeamVariables, awayTeamVariables)

            error = y - y_est
            log_likelihood = self.calc_log_likelihood(error, variance)
            total_log_likelihood = total_log_likelihood + log_likelihood

            tot_error += error
            # bereken de likelihood dat een observatie voorkomt

        avg_error = tot_error / len(match_train)
        self.avg_error_timeline.append(avg_error)

        print("totlikelihood", round(total_log_likelihood, 5), end=" ")
        print(avg_error)

        return -total_log_likelihood
