from config import API_KEY					# get API key from config file
import requests, json, random, datetime
from randomTrivia import randomEntry

random.seed()								# create seed for RNG system
cache = {}									# create cache for storing API response JSON objects
scoreList = []								# list to keep track of scores by year and season type
headers = {"Ocp-Apim-Subscription-Key": API_KEY}		            # header info for the API calls


# function to send news request to API
def sendNewsReq():
    timeNow = datetime.datetime.now()
    if (cache.get("newsTTL") == None or cache["newsTTL"] < timeNow):    # runs API call if cache DNE or is stale
        print("Get news API call started")

        req = requests.get("https://api.sportsdata.io/v3/nfl/scores/json/News", headers=headers)

        if (req.status_code == 200):
            print("Get players API call succeeded")
            cache["news"] = json.loads(req.text)                        # cache JSON object to "news"
            cache["newsTTL"] = timeNow + datetime.timedelta(days=30)    # cache TTL (time-to-live)
        else:
            print("Get news API call failed")
    

# helper function for newsView in main to get news object from API
def getNews():
    obj = None
    sendNewsReq()
    if (cache.get("news") != None):
        obj = randomEntry(cache["news"])
        
    return obj    

    