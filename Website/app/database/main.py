"""
Database Functions

update_users(user)
/*@requires type(user) == dict &&
            len(user) == 3 &&
            type(user["user_id"]) == string &&
            type(user["username"]) == str &&
            type(user["total"]) == float
            type(user["password_hash"]) == str @*/
//@ensures user in data.json

new_user_bets(user_bet)
/*@requires type(user_bet) == dict &&
            len(user_bet) ==  4&&
            type(user_bet["user_id"]) == string &&
            type(user_bet["bet_id"]) == string &&
            type(user_bet["team"]) == string &&
            type(user_bet["value"]) == float @*/
//@requires user_bet["team"] in (bet["bet_id"]["team1"], bet["bet_id"]["team2"])
//@ensures user_bet in data.json

update_bets()
//@ensures all data and bets are up to date

DATABASE FORMAT: (retrieve_database() returns dict)
database (dict)
     "users" (dict)
        retrieve user using user_id in string form (dict)
          "username" (string)
          "total" (float)
          "total-history" (list of tuples -- (time, result))
     "user-bets" (dict)
        retrieve list of bets from each user using user_id in string form (list)
          for each element (dict):
            "bet_id" (str)
            "team" (str)
            "value" (float)
            "winnings" (float)
            "net" (float)
            "timestamp" (float)
     "bets" (dict)
        retrieve bet using bet_id in string form (dict)
          "team1" (string)
          "team2" (string)
          "line1" (float)
          "line2" (float)
          "odds1" (float)
          "odds2" (float)
          "winner" (string -- "None" if no winner yet)
          "timestamp" (int)

"""

import json, time, copy
import random
from scrape import *


def intify(text):
    if type(text) == int:
        return text
    if text == "pk":
        return 0
    if text[0] == "+":
        text = text[1:]
    if text[-1] == "½":
        text = text[:-1] + ".5"
    return float(text)


def retrieve_database(filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        return data


def update_users(user, filepath):
    new_user = copy.deepcopy(user)
    new_user.pop("user_id")
    new_user["total-history"] = []
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        if user["user_id"] in data["users"]:
            return
        data["users"][user["user_id"]] = new_user
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_user_by_id(user_id, filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        if user_id in data["users"]:
            return data["users"][user_id]


def get_user_by_name(username, filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        for user_id in data["users"]:
            if data["users"][user_id]["username"] == username:
                curr_user = copy.deepcopy(data["users"][user_id])
                curr_user["user_id"] = user_id
                return curr_user


def get_user_bets(user_id, filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        if user_id in data["user-bets"]:
            return data["user-bets"][user_id]


def update_bets(league, filepath):
    raw = websiteScraping(league)
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        for point in raw:
            bet = {}
            if type(point) == list:
                bet_id = str(format(0, '06d'))
                for check in data["bets"][league]:
                    if (data["bets"][league][check]["team-1"] == point[0] and
                            data["bets"][league][check]["team-2"] == point[1]):
                        bet_id = check
                if bet_id == "000000":
                    bet_id = str(format(random.randint(1, 999999), '06d'))
                    while bet_id in data["bets"][league]:
                        bet_id = str(format(random.randint(1, 999999), '06d'))
                bet["team-1"] = point[0]
                bet["team-2"] = point[1]
                bet["line1"] = intify(point[-2][0])
                bet["line2"] = intify(point[-2][1])
                bet["odds1"] = intify(point[2][0])
                bet["odds2"] = intify(point[2][1])
                bet["winner"] = "None"
                bet["timestamp"] = time.time()
                data["bets"][league][bet_id] = bet
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def new_user_bets(user_bet, filepath):
    bet = copy.deepcopy(user_bet)
    bet.pop("user_id")
    bet["timestamp"] = time.time()
    bet["winnings"] = user_bet["value"]
    bet["net"] = 0
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        if user_bet["user_id"] in data["user-bets"]:
            data["user-bets"][user_bet["user_id"]].append(bet)
        else:
            data["user-bets"][user_bet["user_id"]] = [bet]
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def conclude_bet(bet_id, filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        curr_league = "NCAA"
        for league in data["bets"]:
            if bet_id in data["bets"][league]:
                curr_league = league
                break
        if data["bets"][curr_league][bet_id]["winner"] != "None":
            return
        winner = random.choice([data["bets"][curr_league][bet_id]["team-1"],
                                data["bets"][curr_league][bet_id]["team-2"]])
        data["bets"][curr_league][bet_id]["winner"] = winner
        for user in data["user-bets"]:
            for bet in data["user-bets"][user]:
                if bet["bet_id"] == bet_id:
                    if (data["user-bets"][user][bet_id]["team"] == data[
                        "bets"][curr_league][bet_id]["winner"]):
                        if (data["bets"][curr_league][bet_id]["winner"] ==
                            data["bets"][curr_league][bet_id]["team-1"]):
                            data["user-bets"][user][bet_id]["net"] = (data["user-bets"][user][bet_id]["value"]
                                   /abs(data["bets"][curr_league][bet_id][
                                            "odds1"]))
                        else:
                            data["user-bets"][user][bet_id]["net"] = (data["user-bets"][user][bet_id]["value"]
                            / abs(data["bets"][curr_league][bet_id]["odds1"]))
                        data["user-bets"][user][bet_id]["winnings"] = data[
                            "user-bets"][user][bet_id]["net"] + data[
                            "user-bets"][user][bet_id]["value"]
                    else:
                        data["user-bets"][user][bet_id]["net"] = -1 * data["user-bets"][user][bet_id]["value"]
                        data["user-bets"][user][bet_id]["winnings"] = 0
                    data["user-bets"][user][bet_id]["net"] = round(data["user-bets"][user][bet_id]["net"], 2)
                    data["user-bets"][user][bet_id]["winnings"] = round(data["user-bets"][user][bet_id]["winnings"], 2)

def get_bets_by_league(league, filepath):
    return retrieve_database(filepath)["bets"][league]
