cache = {} 

def storeInPlayerRank(key, data):
	cache[key] = data
	print(key, "stored in cache")

def getPlayerRank(key, func1, func2, func3):
	def func(x):
		return x["value"]

	players = cache.get("playerRank")
	if (players == None):
		return None
	results = []
	for i in range(0, len(players)):
		player = players[i]
		if (func1(player) and func2(player) and func3(player)):
			obj = { "name":player["Name"], "value":player[key] }
			results.append(obj)
	return sorted(results, reverse=True, key=func)
