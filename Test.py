from Algorithm import *

class Test:
    '''Test is an object which contains all analysis of an executed algorithm of object Algorithm, based on a given test dataset.
         It shows the average error, how many per cent of the matches can be predicted correctly and how the model can make (or lose) money when using it to bet on bettingsides.'''
    algorithm=None
    coefficients=[]
    match_test=[]

    avg_error=0
    avg_correct_prediction=0
    capital=10000

    def __init__(self,algorithm,match_test):
        self.algorithm=algorithm
        self.coefficients = algorithm.coefficients
        self.match_test = match_test

        self.avg_error,self.avg_correct_prediction=self.total_error()
        self.capital=self.compete_with_bookmakers()


    def total_error(self):
        '''This method calculates how accurate the established model is. It returns 2 things:
           The average error between the estimated result and the official result.
           And how many per cent of the games are predicted correctly by the algorithm.'''
        tot_prediction = 0
        tot_error = 0
        for match in self.match_test:
            y = match.won
            homeTeam = match.home_team
            awayTeam = match.away_team
            homeTeamVariables, awayTeamVariables = self.algorithm.create_variables(homeTeam, awayTeam, match)
            if type(self.algorithm) == Linear_regression:
                y_est = self.algorithm.calc_linear_regression(self.coefficients, homeTeamVariables, awayTeamVariables)
            elif type(self.algorithm) == Neural_network:
                y_est = self.algorithm.calc_neural_network(homeTeamVariables, awayTeamVariables)


            correct_prediction = self.calc_correct_prediction(y_est, y)
            tot_prediction += correct_prediction
            error = self.calc_error(y_est, y)
            tot_error += error
        avg_error = "average error " + str(tot_error / len(self.match_test))
        avg_correct_prediction = "amount of games predicted right  " + str(1 - (tot_prediction / len(self.match_test)))

        return avg_error, avg_correct_prediction

    def calc_correct_prediction(self,y_est,y):
        res=(y_est>0.5)==y
        return int(res)

    def calc_error(self,y_est,y):
        res=math.fabs(y-y_est)
        return res


    def compete_with_bookmakers(self):
        '''This method calculates how much many you can make using the model to bet on games.
           It compares the established odds from the algorithm with official odds of bookmakers.
           When the established odds are predicting a team will win or lose better than the official odds, than it will bet on the 'winning' team.'''
        capital=10000
        for match in self.match_test:
            homeTeam = match.home_team
            awayTeam = match.away_team
            won=match.won
            homeTeamVariables, awayTeamVariables = self.algorithm.create_variables(homeTeam, awayTeam, match)
            constante = self.coefficients[0]
            variance = self.coefficients[-1]

            if type(self.algorithm)==Linear_regression:
                y_est = self.algorithm.calc_linear_regression(self.coefficients,homeTeamVariables,awayTeamVariables)
            elif type(self.algorithm)==Neural_network:
                y_est = self.algorithm.calc_neural_network(homeTeamVariables,awayTeamVariables)


            # nu bereken je de kans dat de error van verliezen voorkomt, en de kans dat de error van winnen voorkomt (gegeven een distribution)
            estimated_odd=self.get_estimated_winning_odd(y_est,variance)

            official_odd,official_return=self.get_official_bettingData(match)

            capital=self.bet(capital,estimated_odd,official_odd,official_return,won)

        return capital

    def get_estimated_winning_odd(self,y_est,variance):
        '''This method converts the outcome of the algorithm to a how much more likely the hometeam is to win.
           Dividing the likelihood of winning by the likelihood of losing results in an odd for the hometeam. '''
        error_winst = math.fabs(y_est - 1)
        error_verlies = math.fabs(y_est - 0)
        log_likelihood_winst = self.algorithm.calc_log_likelihood(error_winst, variance)
        log_likelihood_verlies = self.algorithm.calc_log_likelihood(error_verlies, variance)
        likelihood_winst = math.e ** (log_likelihood_winst)
        likelihood_verlies = math.e ** (log_likelihood_verlies)
        estimated_odd = likelihood_winst / likelihood_verlies
        return estimated_odd

    def get_official_bettingData(self,match):
        '''This method returns the official odds and returns from official bookmakers.
           The odds are calculated by dividing 1 by the return.
           Bookmaker: 'bwin' '''
        official_return = match.oddsHomeTeam  # how much more money you get back if you win
        implied_win_probability = 1 / official_return
        implied_lose_probability = 1 - implied_win_probability
        official_odd=(implied_win_probability / implied_lose_probability)   # how much more likely is the hometeam to win
        return official_odd,official_return

    def bet(self,capital,estimated_odd,official_odd,official_return,won):
        '''This method will bet based on official odds and the prediction odds.
           If the predicted odd for the favorite team is higher than that of bookmakers, it will bet 100 euro's on the favorite team.
           Starting capital=100'''
        if estimated_odd > 1:
            if official_odd < estimated_odd:
                capital -= 100
                if won == 1:
                    capital += official_return * 100


        return capital

    def save(self, name):
        with open(name+".pickle", "wb") as f:
            pickle.dump(self, f)

    def load(self,name):
        with open(name+".pickle", "rb") as f:
            newObj = pickle.load(f)
            self.__dict__.update(newObj.__dict__)