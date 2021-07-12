import random, datetime
from teamAbbrevs import teamAbbrev

random.seed()								# create seed for RNG system
cache = {}									# create cache for storing API response JSON objects

# function to process a JSON object and returns a random attribute-value object
def randomEntry(obj):
	if (obj and len(obj) > 0):
		randomNum = random.randint(0, len(obj) - 1)
		return obj[randomNum]
	else:
		return obj

# function to process a date string XXXXTXXXX to return only the field before T
def getDate(dateStr):
	if (dateStr):							# if not None
		return dateStr.split("T")[0]
	else:
		return dateStr						# return None

# function to process a date string XXXXTXXXX to return only the field after T to get time
def getTime(dateStr):
	if (dateStr):							# if not None
		dateStr = dateStr.split("T")
		if (len(dateStr) > 1):				# if object is empty
			return dateStr[1]				# return the field after T
		else:
			return "TBD"					# return "To Be Determined"
	else:
		return dateStr						# return None

# function to process a seasonType (1, 2, 3) and return the season type in string
def getSeasonType(seasonType):
	if (seasonType):
		if (seasonType == 1):
			return "Regular season"
		elif (seasonType == 2):
			return "Preseason"
		else:
			return "Postseason"

# function to store a JSON object into cache
def storeInRandomTrivia(key, data):
	cache[key] = data
	print(key, "stored in cache")

# function to get a list of score keys stored in cache
def getScoreList(startYear):
	scoreList = []
	currentYear = datetime.datetime.now().year		# get the current year
	while (startYear <= currentYear):				# loop until greater than current year
		if (cache.get(str(startYear) + "Score") != None):
			scoreList.append(str(startYear) + "Score")
		if (cache.get(str(startYear) + "PREScore") != None):
			scoreList.append(str(startYear) + "PREScore")
		if (cache.get(str(startYear) + "POSTScore") != None):
			scoreList.append(str(startYear) + "POSTScore")
		startYear += 1
	return scoreList

# helper function for randomView in main to get object of either a random player or random game
def getRandomTrivia():
	obj = None								# init obj
	randomNum = random.randint(0, 1)		# get a random number between 0 and 1
	if (randomNum):							# when 1 then show a random player to user
		if (cache.get("players") != None):				# players API call could have failed, then cache will not have "players"
			obj = randomEntry(cache["players"])			# get a players JSON object from cache and then get a random player
			obj["BirthDate"] = getDate(obj["BirthDate"])			# process the date
			currTeam = teamAbbrev.get(obj["CurrentTeam"])			# convert team abbreviation
			if (currTeam):											# may already be converted in JSON from before, then currTeam = None
				obj["CurrentTeam"] = currTeam
	else:									# show a random game to user
		scoreList = getScoreList(2018)		# scoreList contains keys to get score from cache
		if (len(scoreList) > 0):			# scoreList could be empty, make sure it is not
			randomNum2 = random.randint(0, len(scoreList) - 1)		# get a random number between 0 and 1 less than size of scoreList
			obj = randomEntry(cache[scoreList[randomNum2]])			# get a season score JSON object from cache and then get a random game
			obj["SeasonType"] = getSeasonType(obj["SeasonType"])	# process the season type
			obj["Time"] = getTime(obj["Date"])						# process the time
			obj["Date"] = getDate(obj["Date"])						# process the date
			awayTeam = teamAbbrev.get(obj["AwayTeam"])				# convert team abbreviation
			if (awayTeam):					# may already be converted in cache from before, then awayTeam = None
				obj["AwayTeam"] = awayTeam
			homeTeam = teamAbbrev.get(obj["HomeTeam"])				# convert team abbreviation
			if (homeTeam):					# may already be converted in cache from before, then homeTeam = None
				obj["HomeTeam"] = homeTeam
	return obj								# return object for randomView
