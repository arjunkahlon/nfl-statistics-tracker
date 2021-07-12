# OSU CS 361 Winter 2020 Team 1's Agile Project
# by
# Jennifer Banks
# Arjun Kahlon
# Cameron Jones
# Corbin Tegner
# Kevin Wu
# Roman Guerrero
#
# This project is a website for retrieving useful NFL statistics. Currently,
# the website supports getting NFL statistics such as: random league trivia,
# ....

from flask import Flask, render_template, url_for, redirect, request, Response
from forms import TeamForm # form for team schedule search
from randomTrivia import getRandomTrivia, storeInRandomTrivia	# get functions for random trivia
from teamSchedule import getTeamSchedule
from teamScores import getWeekScore
from standings import getStandings
from news import getNews
from playerRank import getPlayerRank, storeInPlayerRank
from teamStats import createListByAttributes, storeInTeamStats	# get functions for team stats
from config import PORT, API_KEY							# get port, api key from config file
import json
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba249' #secret key for forms
logging.basicConfig(filename="service.log", level=logging.DEBUG)

# for handling post methods
def postMethod(func):
	obj = json.loads(request.data)							# convert data to JSON object
	if (obj["api_key"] == API_KEY):							# verify authentication, reusing sportsdataIO api key
		print("Authorized POST request received")
		logging.info("Authorized POST request received")
		obj = json.loads(request.data)
		func(obj["data_type"], obj["data"])					# store JSON into cache depending on func function
		return Response(status=200)							# return response
	else:
		print("Unauthorized POST request received")
		logging.warning("Unauthorized POST request received")
		return Response(status=401)							# return unauthorized response

# home view
@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

# about view
@app.route("/about")
def about():
	return render_template("about.html")

# random view
@app.route("/random", methods=("GET", "POST"))				# post method for worker to send JSON objects
def randomView():
	if (request.method == "POST"):
		return postMethod(storeInRandomTrivia)
	else:
		obj = getRandomTrivia()
		return render_template("random.html", object=obj)	# return rendering to user

# team schedule view
@app.route("/teamSchedule", methods=('GET', 'POST'))
def teamScheduleView():
	form = TeamForm()  # form class
	team = None
	if form.validate_on_submit():
		team = form.teamName.data
	obj = getTeamSchedule(team)
	return render_template('teamSchedule.html', form=form, object=obj)

# news view
@app.route("/news")
def newsView():
	obj = getNews()
	return render_template("news.html", object=obj)	# return rendering to user

# route for storing team stats data
@app.route("/teamStats", methods=(["POST"]))				# post method for worker to send JSON objects
def teamStats():
	return postMethod(storeInTeamStats)

# offensive team stats
@app.route("/offenseStats")
def offenseView():
	obj = createListByAttributes("OffensiveYards", "PassingYards", "RushingYards", "offense")
	if (obj == None):
		return render_template("offenseStats.html")
	return render_template("offenseStats.html", offensive=obj[0], passing=obj[1], rushing=obj[2])

# team score view
@app.route("/teamScores", methods=('GET', 'POST'))
def teamScoreView():
	form = TeamForm()  # form class
	team = None
	if form.validate_on_submit():
		team = form.teamName.data
	obj = getWeekScore(team)
	return render_template('teamScores.html', form=form, object=obj)

# team standings view
@app.route("/standings")
def standings():
	obj = getStandings()
	return render_template("standings.html", object=obj)

# route for storing player rank data
@app.route("/playerRank", methods=(["POST"]))				# post method for worker to send JSON objects
def playerRank():
	return postMethod(storeInPlayerRank)

# QB completion view
@app.route("/qbCompletion")
def players():
	def func1(player):
		return player["Position"] == "QB"

	def func2(player):
		return player["PassingCompletionPercentage"] <= 100

	def func3(player):
		return player["Started"] > 0

	obj = getPlayerRank("PassingCompletionPercentage", func1, func2, func3)
	if (obj == None):
		return render_template("qbc.html")
	return render_template("qbc.html", len=len(obj), objects=obj)

# flask server setup
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=PORT)
