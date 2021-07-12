from config import API_KEY, PORT
import requests, json, datetime, time
import logging

cache = {}								# TTL cache
sleepTimeInSeconds = 10					# seconds to sleep, not permanently set
connectionError = 0						# keeps tracks how many API calls failed in each cycle
connectionAttempts = 0					# keeps tracks total number of API calls in each cycle
cycleCount = 0							# keeps track of number of consecutive cycles of at least one API call failure
headers = {"ocp-apim-subscription-key": API_KEY}		# header info for the API calls
logging.basicConfig(filename="worker.log", level=logging.DEBUG)

# function to get player stats using API call and then storing TTL in cache
def getPlayers():
	global connectionError, connectionAttempts
	timeNow = datetime.datetime.now()					# get current time
	playersTTL = cache.get("players")					# get TTL from cache
	if (playersTTL == None or playersTTL < timeNow):	# API call if cache not exist or is stale
		print("Get players API call started")
		logging.info("Get players API call started")
		try:
			connectionAttempts += 1						# increment total numbef of API calls in this cycle
			req = requests.get("https://api.sportsdata.io/v3/nfl/scores/json/Players", headers=headers)
			if (req.status_code == 200):				# 200 = success
				print("Get players API call succeeded")
				logging.info("Get players API call succeeded")
				cache["players"] = timeNow + datetime.timedelta(days=30)	# cache TTL
				obj = json.loads(req.text)				# get JSON object
				postData("players", "random", obj)		# send JSON to server
			else:
				print("Get players API call failed")
				logging.warning("Get players API call failed")
		except requests.exceptions.RequestException as e:	# generalized request exception catch
			connectionError += 1						# increment total number of failed API call in this cycle
			print("Connection Error (", connectionError, "/", connectionAttempts, ")", sep="")
			logging.warning("Connection Error (" + str(connectionError) + "/" + str(connectionAttempts) + ")")

# function to get a score by year and season type using API calls and then store result in cache
def getScore(year, seasonType):
	global connectionError, connectionAttempts
	timeNow = datetime.datetime.now()					# get current time
	scoreTTL = cache.get(year + seasonType + "Score")	# get TTL from cache
	if (scoreTTL == None or scoreTTL < timeNow):		# API call if cache not exist or is stale
		print("Get score API call started for", year, seasonType)
		logging.info("Get score API call started for " + year + " " + seasonType)
		try:
			connectionAttempts += 1						# increment total numbef of API calls in this cycle
			req = requests.get("https://api.sportsdata.io/v3/nfl/scores/json/Scores/" + year + seasonType, headers=headers)
			if (req.status_code == 200):				# 200 = success
				print("Get score API call succeeded for", year, seasonType)
				logging.info("Get score API call succeeded for " + year + " " + seasonType)
				cache[year + seasonType + "Score"] = timeNow + datetime.timedelta(days=7)	# cache TTL
				obj = json.loads(req.text)				# get JSON object
				if (len(obj) > 0):						# send to server only if obj has content
					postData(year + seasonType + "Score", "random", obj) # send JSON to server
			elif (req.status_code == 401):				# unauthorized request
				cache[year + seasonType + "Score"] = timeNow + datetime.timedelta(days=30)	# cache TTL to not call again for now
				print("Get score API call failed (unauthorized) for", year, seasonType)
				logging.warning("Get score API call failed (unauthorized) for " + year + " " + seasonType)
			else:
				print("Get score API call failed for", year, seasonType)
				logging.warning("Get score API call failed for " + year + " " + seasonType)
		except requests.exceptions.RequestException as e:	# generalized request exception catch
			connectionError += 1						# increment total number of failed API call in this cycle
			print("Connection Error (", connectionError, "/", connectionAttempts, ")", sep="")
			logging.warning("Connection Error (" + str(connectionError) + "/" + str(connectionAttempts) + ")")

# function to try to get scores from various years and seasons
def getAllScoreFrom(startYear):
	currentYear = datetime.datetime.now().year			# get the current year
	while (startYear <= currentYear):					# loop until greater than current year
		getScore(str(startYear), "")
		getScore(str(startYear), "PRE")
		getScore(str(startYear), "POST")
		startYear += 1

# function to get team stats using API calls and then store result in cache
def getTeamStats(startYear):
	global connectionError, connectionAttempts
	timeNow = datetime.datetime.now()					# get current time
	teamStatsTTL = cache.get("teamStats")				# get TTL from cache
	if (teamStatsTTL == None or teamStatsTTL < timeNow):	# API call if cache not exist or is stale
		currYear = timeNow.year
		while (currYear >= startYear):					# start a loop to find the most recent season that contains stats
			print("Get team stats API call started for", str(currYear))
			logging.info("Get team stats API call started for " + str(currYear))
			try:
				connectionAttempts += 1					# increment total numbef of API calls in this cycle
				req = requests.get("https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/" + str(currYear), headers=headers)
				if (req.status_code == 200):			# 200 = success
					print("Get team stats API call succeeded for", str(currYear))
					logging.info("Get team stats API call succeeded for " + str(currYear))
					obj = json.loads(req.text)	
					if (len(obj) > 0):					# cache and send to server only if obj has content
						cache["teamStats"] = timeNow + datetime.timedelta(days=7)	# cache TTL
						postData("teamStats", "teamStats", obj)	# send JSON to server
						break;							# got data, end loop
				else:
					print("Get team stats API call failed for", str(currYear))
					logging.warning("Get team stats API call failed for	" + str(currYear))
			except requests.exceptions.RequestException as e:	# generalized request exception catch
				connectionError += 1					# increment total number of failed API call in this cycle
				print("Connection Error (", connectionError, "/", connectionAttempts, ")", sep="")
				logging.warning("Connection Error (" + str(connectionError) + "/" + str(connectionAttempts) + ")")
			currYear -= 1								# try a previous year

def getPlayerRank(startYear):
	global connectionError, connectionAttempts
	timeNow = datetime.datetime.now()					# get current time
	playerRankTTL = cache.get("playerRank")				# get TTL from cache
	if (playerRankTTL == None or playerRankTTL < timeNow):	# API call if cache not exist or is stale
		currYear = timeNow.year
		while (currYear >= startYear):					# start a loop to find the most recent season that contains stats
			print("Get player rank API call started for", str(currYear))
			logging.info("Get player rank API call started for " + str(currYear))
			try:
				connectionAttempts += 1					# increment total numbef of API calls in this cycle
				req = requests.get("https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/" + str(currYear), headers=headers)
				if (req.status_code == 200):			# 200 = success
					print("Get player rank API call succeeded for", str(currYear))
					logging.info("Get player rank API call succeeded for " + str(currYear))
					obj = json.loads(req.text)	
					if (len(obj) > 0):					# cache and send to server only if obj has content
						cache["playerRank"] = timeNow + datetime.timedelta(days=7)	# cache TTL
						postData("playerRank", "playerRank", obj)	# send JSON to server
						break;							# got data, end loop
				else:
					print("Get player rank API call failed for", str(currYear))
					logging.warning("Get player rank API call failed for	" + str(currYear))
			except requests.exceptions.RequestException as e:	# generalized request exception catch
				connectionError += 1					# increment total number of failed API call in this cycle
				print("Connection Error (", connectionError, "/", connectionAttempts, ")", sep="")
				logging.warning("Connection Error (" + str(connectionError) + "/" + str(connectionAttempts) + ")")
			currYear -= 1								# try a previous year

# function to send POST request to server to send JSON object
def postData(key, route, obj):
	global connectionError, connectionAttempts
	payload = {"api_key":API_KEY, "data_type":key, "data":obj}	# reuse sportsdataIO api key 
	print("Post API call from worker started for", key)
	logging.info("Post API call from worker started for " + key)
	try:
		connectionAttempts += 1							# increment total numbef of API calls in this cycle
		req = requests.post("http://flip3.engr.oregonstate.edu:" + str(PORT) + "/" + route, json.dumps(payload))
		if (req.status_code == 200):
			print("Post API call from worker succeeded")
			logging.info("Post API call from worker succeeded")
		else:
			print("Post API call from worker failed")
			logging.warning("Post API call from worker failed")
	except requests.exceptions.RequestException as e:	# generalized request exception catch
		connectionError += 1							# increment total number of failed API call in this cycle
		print("Connection Error (", connectionError, "/", connectionAttempts, ")", sep="")
		logging.warning("Connection Error (" + str(connectionError) + "/" + str(connectionAttempts) + ")")
		cache[key] = datetime.datetime.now()	# set the TTL to now, so next cycle TTL will be outdated

while (1):
	connectionError = 0					# reset number of connection errors in this cycle
	connectionAttempts = 0				# reset number of API calls in this cycle
	cycleCount += 1						# increment number of consecutive cycles of at least one API call failure
	timeNow = datetime.datetime.now()	# get current time
	print(timeNow)
	logging.info(timeNow)

	getPlayers()						# get players
	getAllScoreFrom(2018)				# get scores
	getTeamStats(2018)					# get team stats
	getPlayerRank(2018)
	
	if (connectionError == 0):			# no connection errors in this cycle
		sleepTimeInSeconds = 3600		# sleep longer
		cycleCount = 0					# reset number of consecutive cycles of at least one API call failure
	else:
		sleepTimeInSeconds = 10			# at least one connect failure = sleep for 10 seconds only
		if (cycleCount == 10):			# if number of consecutive cycles of at least one API call failure is 10, break loop
			break
	print("Sleeping for", sleepTimeInSeconds, "seconds.")
	logging.info("Sleeping for " + str(sleepTimeInSeconds) + " seconds.")
	time.sleep(sleepTimeInSeconds)		# sleep
	print("Slept for", sleepTimeInSeconds, "seconds and now I'm awake.")
	logging.info("Slept for " + str(sleepTimeInSeconds) + " seconds and now I'm awake.")
