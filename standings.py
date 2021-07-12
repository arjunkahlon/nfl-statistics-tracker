from config import API_KEY					# get API key from config file
from flask_table import Table, Col, LinkCol
import requests, json, random, datetime

cache = {}							# create cache for storing API response JSON objects
headers = {"ocp-apim-subscription-key": API_KEY}		# header info for the API calls

# Info for sortable table from Flask
'''class SortableTable(Table):
        id = Col('ID')
    name = Col('Name')
    description = Col('Description')
    link = LinkCol(
        'Link', 'flask_link', url_kwargs=dict(id='id'), allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)'''



# function to get standings (2019 regular season)
def standingsReq():
	req = requests.get("https://api.sportsdata.io/v3/nfl/scores/json/Standings/2019REG", headers=headers)
	if (req.status_code == 200):
		print("Standings API call succeeded.")
		cache["standings"] = json.loads(req.text)
	else:
		print("Standings API call failed.")



#Function to feed APO data to object
def getStandings():
	obj = None
	standingsReq()
	if (cache.get("standings") != None):
		obj = cache["standings"]
	return obj 


#Function to sort teams by win percentage
def sortStandings():
	obj = getStandings()
	obj.sort(key=obj.Percentage, reverse=True)
	return obj