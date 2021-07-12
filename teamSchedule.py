from config import API_KEY
from teamAbbrevs import teamAbbrev
import requests, json, datetime

headers = {"ocp-apim-subscription-key": API_KEY}

def populateObj(team_week):
    
    week = {"weekNum":" ", "HomeTeam":" ", "AwayTeam":" ", "City":" ", "State":" "}
    if (team_week["StadiumDetails"] != None):
        week["weekNum"] = team_week["Week"]
        week["HomeTeam"] = teamAbbrev[team_week["HomeTeam"]]
        week["AwayTeam"] = teamAbbrev[team_week["AwayTeam"]]
        week["City"] = team_week["StadiumDetails"]["City"]
        week["State"] = team_week["StadiumDetails"]["State"]
        
    else:
        week["weekNum"] = team_week["Week"]
        week["HomeTeam"] = "BYE"
        week["AwayTeam"] = "WEEK"
        week["City"] = " "
        week["State"] = " "         # spaces here so that the element is not null
    return week

def getTeamSchedule(name):
    curr_team = name
    obj = {"tName":name, "week1":"N/A", "week2":"N/A", "week3":"N/A", "week4":"N/A", "week5":"N/A", "week6":"N/A", "week7":"N/A", "week8":"N/A",
            "week9":"N/A", "week10":"N/A", "Week11":"N/A", "week12":"N/A", "week13":"N/A", "week14":"N/A", "week15":"N/A", "Week16":"N/A", "week17":"N/A"}
    req = requests.get('https://api.sportsdata.io/v3/nfl/scores/json/Schedules/2019',headers = headers)
    teams = json.loads(req.text)
    team_schedule = []
    for item in range (0, len(teams)):                  # this loop will put 17 items in the team_schedule array
        if (teams[item]["AwayTeam"] == curr_team):
            team_schedule.append(teams[item])
        elif (teams[item]["HomeTeam"] == curr_team):
            team_schedule.append(teams[item])

    if(curr_team != None):
        # populate the object with all the info
        obj["tName"] = teamAbbrev[name]
        obj["week1"] = populateObj(team_schedule[0])
        obj["week2"] = populateObj(team_schedule[1])
        obj["week3"] = populateObj(team_schedule[2])
        obj["week4"] = populateObj(team_schedule[3])
        obj["week5"] = populateObj(team_schedule[4])
        obj["week6"] = populateObj(team_schedule[5])
        obj["week7"] = populateObj(team_schedule[6])
        obj["week8"] = populateObj(team_schedule[7])
        obj["week9"] = populateObj(team_schedule[8])
        obj["week10"] = populateObj(team_schedule[9])
        obj["week11"] = populateObj(team_schedule[10])
        obj["week12"] = populateObj(team_schedule[11])
        obj["week13"] = populateObj(team_schedule[12])
        obj["week14"] = populateObj(team_schedule[13])
        obj["week15"] = populateObj(team_schedule[14])
        obj["week16"] = populateObj(team_schedule[15])
        obj["week17"] = populateObj(team_schedule[16])

    return obj
