class Match:
  home_team = 'None'
  away_team = 'None'
  won = -1 # 1 = home team, 0 = out team, 0.5 = draw
  date = ""
  league = ""

  def __init__(self, home_team_name,away_team_name,won,date,league):
      self.home_team = home_team_name
      self.away_team = away_team_name
      self.won = won
      self.date = date
      self.league = league

  def updateTeams(self,home_team,away_team):
      self.home_team=home_team
      self.away_team=away_team
