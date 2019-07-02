import math
from scipy import optimize
import numpy as np
import pickle
from matplotlib import pyplot

class Algorithm:
    '''All algorithms which belong to 'Algorithm' build a model which predicts the outcome of matchresults.
       The prediction is based on the likelihood of the occurrence of the error between the outcomes of the model and the official result of matches.'''
    method='Nelder-Mead'
    opt = {'maxiter': 10000, 'adaptive': False}
    model = None
    avg_error_timeline=[]


    def __init__(self):
        pass


    def create_variables(self,homeTeam, awayTeam, match):
        ''' this creates the variables for both the hometeam and the awayteam and returns them in 2 lists. The variables are:
            average age
            average height
            average weight
            average rating attackers
            average rating midfielders
            average rating defenders
            average rating goalkeepers
            amount of rest days since the last game
            '''
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




    def calc_log_likelihood(self,error, variance):
        '''This method calculates the natural logarithm of how likely a the predicted game result is to approaching the official result.
           The fact that the natural logarithm of X is always increasing when X increases makes it possible to maximise the likelihood with the loglikelihood.
           This makes it easier to calculate over multiple values.

           '''
        try:
            return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (variance)
            # return - (1 / 2) * math.log(2 * math.pi , math.e) - (1/2) * math.log(variance, math.e) - ((error**2)/(2*variance))
        except Exception:
            print(variance, error)
            return -(1 / 2) * math.log(2 * math.pi * (variance), math.e) - (1 / 2) * ((error) ** 2) / (
                    variance + 0.001)

    def save(self, name):
        '''This method saves the algorithm object as a pickle file.'''
        with open(name+".pickle", "wb") as f:
            pickle.dump(self, f)

    def load(self,name):
        '''This method opens an algorithm object where the filename is equal to the given parameter.'''
        with open(name+".pickle", "rb") as f:
            newObj = pickle.load(f)
            self.__dict__.update(newObj.__dict__)

    def plot_errors(self):
        '''This method shows a plot of the progression of the error between predicted match results and real match results.
           While training the data, errors are registered to be shown in a graph.'''
        x_values=[]
        y_values=self.avg_error_timeline
        for i in range(len(y_values)):
            x_values.append(i)
        pyplot.scatter(x_values,y_values,5)
        pyplot.show()







class Neural_network(Algorithm):
    '''The algorithm Neural Network predicts the outcome of matches with and input layer(variables), a hidden layer(size=3) and an output layer.
       This algorithm assumes there is no direct relation between variables and the outcome.'''

    match_train=[]
    coefficients=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1, 1]
    tol = 1e-1

    def __init__(self,match_train):
        self.match_train=match_train
        self.coefficients=self.get_nn_coefficients(3)

    def get_nn_coefficients(self,hiddenlayer_size):
        '''This method converts the coefficients used for linear regression to coefficients used for a Neural Network.
           It returns a list with enough coefficients to create the matrixes used for establishing a Neural Network model.'''
        from_variables_to_hidden_layer = self.coefficients[1:-1] * 3
        from_hidden_layer_to_output = [0.1] * hiddenlayer_size
        return [self.coefficients[0]] + from_variables_to_hidden_layer + from_hidden_layer_to_output + [self.coefficients[-1]]

    def calc_neural_network(self, coefficients, homeTeamVariables, awayTeamVariables):
        '''This method converts coefficients to coefficients in matrixes, which are part of the Neural Network with one hidden layer of size: 3.'''
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
        '''This method calls the total_log_likelihood method and tries to minimize the return of that method.
           While doing that it keeps score of the average error of each improved model. '''
        self.avg_error_timeline=[]
        coefficient_initialization = self.coefficients

        model = optimize.minimize(self.total_log_likelihood, coefficient_initialization, args=(self.match_train),
                                  method=self.method,options=self.opt,tol=self.tol)
        self.model=model




    def total_log_likelihood(self, coefficients, match_test):
        '''This method calculates the sum of the loglikelihood of the established linear regression model.
           The total loglikelihood represents how likely it is that all values are approaching the correct values.
           To easy things up, loglikelihood has been used instead of likelihood so the loglikelihoods can be added.'''
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

            y_est = self.calc_neural_network(coefficients,homeTeamVariables,awayTeamVariables)

            error = math.fabs(y - y_est)
            log_likelihood = self.calc_log_likelihood(error, variance)
            total_log_likelihood = total_log_likelihood + log_likelihood

            tot_error += error

        avg_error = tot_error / len(match_test)
        self.avg_error_timeline.append(avg_error)

        print("totlikelihood", round(total_log_likelihood, 5), end=" ")
        print(avg_error)

        return -total_log_likelihood







class Linear_regression(Algorithm):
    '''Linear Regression builds a model which predicts the outcome of matches with a straight line through a n-dimensional space (where n=amount of variables involved).
       This model assumes there is a linear correlation between the increase and decrease of certain variables and the increase of the outcome.
    '''
    match_train=[]
    coefficients=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1]
    tol = 1e-1

    def __init__(self,match_train):
        self.match_train=match_train


    def calc_linear_regression(self,coefficients, homeTeamVariables, awayTeamVariables):
        '''This function calculates the estimated value for y (1=winning, 0=losing) based on variables, coefficients and a constant value.
           The estimation of y is being calculated with linear regression.
           The formula is constructed by the home advantage and the sumproduct of the variable diffences between the hometeam and the awayteam.'''
        y_est = coefficients[0]
        for i in range(1, len(homeTeamVariables) + 1):
            y_est += (coefficients[i] * (homeTeamVariables[i - 1] - awayTeamVariables[i - 1]))
        return y_est


    def minimize_model(self):
        '''This method calls the total_log_likelihood method and tries to minimize the return of that method.
           While doing that it keeps score of the average error of each improved model. '''
        self.avg_error_timeline=[]
        coefficient_initialization = self.coefficients
        model = optimize.minimize(self.total_log_likelihood, coefficient_initialization, args=(self.match_train),
                                  method=self.method,options=self.opt,tol=self.tol)
        self.model = model

        print(model)


    def total_log_likelihood(self, coefficients, match_train):
        '''This method calculates the sum of the loglikelihood of the established linear regression model.
           The total loglikelihood represents how likely it is that all values are approaching the correct values.
           To easy things up, loglikelihood has been used instead of likelihood so the loglikelihoods can be added.'''
        total_log_likelihood = 0
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

            error = math.fabs(y - y_est)
            log_likelihood = self.calc_log_likelihood(error, variance)
            total_log_likelihood = total_log_likelihood + log_likelihood

            tot_error += error

        avg_error = tot_error / len(match_train)
        self.avg_error_timeline.append(avg_error)

        print("totlikelihood", round(total_log_likelihood, 5), end=" ")
        print(avg_error)

        return -total_log_likelihood
