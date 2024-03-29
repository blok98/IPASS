class Match:
  '''Match is an object with all relevant data like:
     home_team
     away_team
     won (if the hometeam wins 'won' will be 1, if it's a draw 'won' will be 0.5, if awayteam wins 'won' will be 0)
     date (datetime object)
     league
     oddsHomeTeam (the return value if the hometeam wins, bookmaker=betwin.
     '''
  home_team = 'None'
  away_team = 'None'
  won = -1 # 1 = home team, 0 = out team, 0.5 = draw
  date = ""
  league = ""
  oddsHomeTeam=1


  def __init__(self, home_team_name,away_team_name,won,date,league,oddsHomeTeam):
      self.home_team = home_team_name
      self.away_team = away_team_name
      self.won = won
      self.date = date
      self.league = league
      self.oddsHomeTeam = oddsHomeTeam

  def updateTeams(self,home_team,away_team):
      '''This method converts the hometeam and awayteam from string to Team objects.'''
      self.home_team=home_team
      self.away_team=away_team

  def __str__(self):
      endstr=""
      if self.won==1:
          endstr=str(self.home_team)+ " won the game."
      elif self.won==0:
          endstr=str(self.away_team)+ " won the game."
      elif self.won==0.5:
          endstr="The game ended in a draw."
      return "The match between "+str(self.home_team)+" and "+str(self.away_team)+" that was being played on "+str(self.date)+". "+endstr

