from teamAbbrevs import teamAbbrev			# teamAbbrev contains 1-to-1 mapping of team abbreviations to team names

cache = {}									# create cache for storing API response JSON objects

# function to store a JSON object into cache
def storeInTeamStats(key, data):
	cache[key] = data
	print(key, "stored in cache")

# functon to re-order the entries in the list by shifting entries in position 1 to position 2 in the current list
def shiftOrder(position1, position2, currList, name, value):
	while (position2 > position1):
		currList[position2]["name"] = currList[position2 - 1]["name"]	# shift down the name
		currList[position2]["value"] = currList[position2 - 1]["value"]	# shift down the value
		position2 -= 1						# decrement position
	currList[position1]["name"] = name		# set the name in position 1
	currList[position1]["value"] = value	# set the value in position 2

# function to determine the top team leaders in league by stats
def createListByAttributes(stat1, stat2, stat3, key):
	teams = cache.get("teamStats")
	if (teams == None):						# cache still empty after API call means no data
		return None
	attributeList = [stat1, stat2, stat3]	# list of the stats
	# list of lists of the league leaders, initalized to None and 0
	results = [	[{"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}],
				[{"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}],
				[{"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}, {"name":None, "value":0}] ]
	for i in range(0, len(teams)):			# go through each team in data, if team stats is higher than value, set to value and set name to team
		team = teams[i]
		for j in range(0, 3):
			stat = attributeList[j]			# iterate through the 3 stats
			currList = results[j]			# iterate through the 3 lists
			value = round(team[stat]/team["Games"], 1)		# get the per game average and round to nearest tenths
			name = teamAbbrev[team["Team"]]
			if (value > currList[0]["value"]):				# team stats is higher than the first entry, re-order the entries in list
				shiftOrder(0, 4, currList, name, value)
			elif (value > currList[1]["value"]):			# team stats is higher than the second entry, re-order the entries in list
				shiftOrder(1, 4, currList, name, value)
			elif (value > currList[2]["value"]):			# team stats is higher than the third entry, re-order the entries in list
				shiftOrder(2, 4, currList, name, value)
			elif (value > currList[3]["value"]):			# team stats is higher than the fourth entry, re-order the entries in list
				shiftOrder(3, 4, currList, name, value)
			elif (value > currList[4]["value"]):			# team stats is higher than the last entry, set the last entry
				shiftOrder(4, 4, currList, name, value)
		results.append(currList)
	return results											# return the list of lists of league leaders