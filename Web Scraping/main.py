#02/14/2020
#Web Scraper for Betting Sites

import bs4
import json
from urllib.request import urlopen as uOpen
from bs4 import BeautifulSoup as soup
import requests
import time
from datetime import date

def websiteScraping(league):
    containers = []
    i = 0
    game = []
    team_name = ''
    name_ret = False

    # here we are simply accesing the website and taking all the data from the html
    if(league == "NCAA"):
        url = "https://www.betonline.ag/sportsbook"
    elif(league == "hockey"):
        url = "https://www.betonline.ag/sportsbook/hockey/nhl"
    aClient = requests.get(url)

    # here is where the html is parsed
    page_soup = soup(aClient.text, "html.parser")

    # here we will find and all the games (basketball) that have not yet occurred
    # we will pair the teams that are playing against eachother in a list which will be 
    # stored in another list

    for entry in page_soup.find_all("td", {"class":"col_teamname bdevtt"}):
        for char in entry:
            team_name += char
        team_name = team_name[:-1]
        if(i >= 2):
            containers.append(game)
            game = []
            i = 0
        game.append(team_name)
        team_name = ''
        i += 1
    containers.append(game)

    # here, like the last for loop, we will be collecting the point spreads and odds
    # associated with every team

    j = 0
    spread_count = 0
    teamOneS = ''
    teamTwoS = ''
    point_spreads = ''
    game_spread = ()
    for entry in page_soup.find_all("td", {"class":"odds bdevtt displayOdds"}):
        point_spreads = ''
        for char in entry:
            if(j % 2 == 0):
                point_spreads += char
                spread_count += 1
        if(spread_count == 1):
            teamOneS += point_spreads
            #print(teamOneS)
        elif(spread_count == 2):
            teamTwoS += point_spreads
            game_spread = (teamOneS, teamTwoS)
            #print(game_spread)
            #print(game_spread)
            containers[(j//4)].append(game_spread)
            game_spread = ()
            teamOneS = ''
            teamTwoS = ''
            spread_count = 0
        j += 1
    print(containers)

    # like the last two loops, this one scrapes data but of projected score differences

    point_difs = ''
    k = 0
    dif_count = 0
    teamOneDif = ''
    teamTwoDif = ''
    team_dif = ()
    for entry in page_soup.find_all("td", {"class":"hdcp bdevtt"}):
        point_difs = ''
        for var in entry:
            if(k % 2 == 0):
                point_difs += var
                dif_count += 1
        if(dif_count == 1):
            teamOneDif += point_difs
        elif(dif_count == 2):
            teamTwoDif += point_difs
            team_dif = (teamOneDif, teamTwoDif)
            containers[(k//4)].append(team_dif)
            team_dif = ()
            teamOneDif = ''
            teamTwoDif = ''
            dif_count = 0
        k += 1

    # we now need to acces the date that the games are occurring on so the betting
    # is able to be kept live. insert(0, x)

    date_ret = False
    date = page_soup.find_all("td", {"class":"bdt"})
    date = str(date)
    str_date = ''
    for let in date:
        if(let == ">"):
            date_ret = True
            continue
        elif(let == "<"):
            date_ret = False
            continue
        if(date_ret == True):
            str_date += let
    # this allows us to remove some characters that are not letters or useful 
    # information (extra whitespace and spare bracket)
    str_date = str_date[1:-2]
    containers.insert(0, str_date)

    # next, we nood two access all the game times and save them to their respective lists

    time_stamp = ''
    ite = 1
    for time in page_soup.find_all("td", {"class":"col_time bdevtt"}):
        for char in time:
            time_stamp = char
        containers[ite].append(time_stamp)
        ite += 1
    print(containers)
    return containers

def timeConversion(container):
    time_str = ''
    time_int = 0
    game_times = []
    time_since_epoch = []
    for i in range(1, len(container)):
        time_str = container[i][len(container[i]) - 1]
        time_str = time_str[:2] + time_str[3:6]
        time_int = int(time_str)
        game_times.append(time_int)

    for j in range(0, len(game_times)):
        if(game_times[j] < 1200):
            game_times[j] = game_times[j] + 1200
    
    date = container[0]

    seconds = time.time()
    local_time = time.localtime(seconds)
    hour = local_time.tm_hour
    minute = local_time.tm_min
    curr_time = (hour*100) + minute
    
    for time_slot in game_times:
        if(curr_time < time_slot):
            timeTilGame = time_slot - curr_time
        elif(curr_time > time_slot):
            timeTilGame = 24 - (curr_time - time_slot)
    
        hoursTilGame = timeTilGame//100
        minutesTilGame = timeTilGame % 100

    # this gives the current time of the next most recent game in terms of seconds 
    # since epoch.
        finalTimeTilGame = seconds + (60 * minutesTilGame) + (3600 * hoursTilGame)
        time_since_epoch.append(finalTimeTilGame)

    # we need to make it so that if the finalTimeTilGame is never equal to or less than
    # the current time (meaning that the game ahs started), that we remove it from wherever
    # it is being stored (probably the json file), because betting on that game, will be frozen
    return time_since_epoch
