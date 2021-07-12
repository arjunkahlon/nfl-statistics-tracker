from config import API_KEY
from teamAbbrevs import teamAbbrev
import requests, json, datetime

headers = {"ocp-apim-subscription-key": API_KEY}

def getWeek(game):
    score = {"weekNum":" ", "HomeTeam":" ", "AwayTeam":" ", "HomeQ1":" ", "HomeQ2":" ", "HomeQ3":" ",
    "HomeQ4":" ", "HomeOT":" ", "AwayQ1":" ", "AwayQ2":" ", "AwayQ3":" ", "AwayQ4":" ", "AwayOT":" ",
    "HomeTotal":" ", "AwayTotal":" "}
    
    score["weekNum"] = game["Week"]
    if(game["StadiumDetails"] != None):
        score["weekNum"] = game["Week"]
        score["HomeTeam"] = teamAbbrev[game["HomeTeam"]]
        score["AwayTeam"] = teamAbbrev[game["AwayTeam"]]
        score["HomeQ1"] = game["HomeScoreQuarter1"]
        score["HomeQ2"] = game["HomeScoreQuarter2"]
        score["HomeQ3"] = game["HomeScoreQuarter3"]
        score["HomeQ4"] = game["HomeScoreQuarter4"]
        score["HomeOT"] = game["HomeScoreOvertime"]
        score["HomeTotal"] = game["HomeScore"]
        score["AwayQ1"] = game["AwayScoreQuarter1"]
        score["AwayQ2"] = game["AwayScoreQuarter2"]
        score["AwayQ3"] = game["AwayScoreQuarter3"]
        score["AwayQ4"] = game["AwayScoreQuarter4"]
        score["AwayOT"] = game["AwayScoreOvertime"]
        score["AwayTotal"] = game["AwayScore"]
    
    else:
        score["weekNum"] = game["Week"]
        score["HomeTeam"] = "BYE"
        score["AwayTeam"] = "WEEK"
        score["HomeQ1"] = " "
        score["HomeQ2"] = " "
        score["HomeQ3"] = " "
        score["HomeQ4"] = " "
        score["HomeOT"] = " "
        score["HomeTotal"] = " "
        score["AwayQ1"] = " "
        score["AwayQ2"] = " "
        score["AwayQ3"] = " "
        score["AwayQ4"] = " "
        score["AwayOT"] = " "
        score["AwayTotal"] = " "

    return score



def getWeekScore(name):
    req = requests.get('https://api.sportsdata.io/v3/nfl/scores/json/Scores/2019',headers = headers)
    scores = json.loads(req.text)
    week_score = []
    curr_team = name
    for item in range (0, len(scores)):
        if ((scores[item]["AwayTeam"] == curr_team) or (scores[item]["HomeTeam"] == curr_team)):
            week_score.append(scores[item])
    obj = {"tName":name, "week1":"N/A", "week2":"N/A", "week3":"N/A", "week4":"N/A", "week5":"N/A",
    "week6":"N/A", "week7":"N/A", "week8":"N/A", "week9":"N/A", "week10":"N/A", "Week11":"N/A",
    "week12":"N/A", "week13":"N/A", "week14":"N/A", "week15":"N/A", "Week16":"N/A"}
    if(curr_team != None):
        obj["tName"] = teamAbbrev[name]
        obj["week1"] = getWeek(week_score[0])
        obj["week2"] = getWeek(week_score[1])
        obj["week3"] = getWeek(week_score[2])
        obj["week4"] = getWeek(week_score[3])
        obj["week5"] = getWeek(week_score[4])
        obj["week6"] = getWeek(week_score[5])
        obj["week7"] = getWeek(week_score[6])
        obj["week8"] = getWeek(week_score[7])
        obj["week9"] = getWeek(week_score[8])
        obj["week10"] = getWeek(week_score[9])
        obj["week11"] = getWeek(week_score[10])
        obj["week12"] = getWeek(week_score[11])
        obj["week13"] = getWeek(week_score[12])
        obj["week14"] = getWeek(week_score[13])
        obj["week15"] = getWeek(week_score[14])
        obj["week16"] = getWeek(week_score[15])
    return obj