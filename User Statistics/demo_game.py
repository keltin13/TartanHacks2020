import random
from data import *

def demo_game():
    nba_teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets",
    "Charlotte Hornets", "Chicago Bulls", "Cleveland Caveliers",
    "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", 
    "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
    "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves",
    "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder",
    "Orlando Magic", "Philadelphia 76ers", "Pheonix Suns", 
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs",
    "Toronto Raptors", "Utah Jazz"]

    avg_score = [110, 113, 111, 103, 106, 106, 116, 110, 108,
    106, 118, 110, 116, 115, 113, 112, 120, 112, 116, 105, 111,
    104, 109, 112, 113, 108, 113, 113, 111]

    team1 = random.randint(0, len(nba_teams) - 1)
    a = True
    while (a == True):
        team2 = random.randint(0, len(nba_teams) - 1)
        if (team1 != team2):
            a = False

    odds = avg_score[team1] - avg_score[team2]
    if odds == 0:
        line = "even odds"
    elif odds > 0:
        line = f"{nba_teams[team1]} -{odds}"
    else:
        line = f"{nba_teams[team2]} {odds}"
    
    outcome = random.choice([team1, team2])

    print(nba_teams[team1], nba_teams[team2], line, nba_teams[outcome])
    return (nba_teams[team1], nba_teams[team2], line, nba_teams[outcome])

    

demo_game()