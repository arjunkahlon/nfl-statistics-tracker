from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

teamChoices = [('ARI', 'Arizona Cardinals'), 
                ('ATL', 'Atlanta Falcons'),
                ('BAL', 'Baltimore Ravens'),
                ('BUF', 'Buffalo Bills'),
                ('CAR', 'Carolina Panthers'),
                ('CHI', 'Chicago Bears'),
                ('CIN', 'Cincinnati Bengals'),
                ('CLE', 'Cleveland Browns'),
                ('DAL', 'Dallas Cowboys'),
                ('DEN', 'Denver Broncos'),
                ('DET', 'Detroit Lions'),
                ('GB', 'Green Bay Packers'),
                ('HOU', 'Houston Texans'),
                ('IND', 'Indianapolis Colts'),
                ('JAX', 'Jacksonville Jaguars'),
                ('KC', 'Kansas City Chiefs'),
                ('LAC', 'Los Angeles Chargers'),
                ('LAR', 'Los Angeles Rams'),
                ('LV', 'Las Vegas Raiders'),
                ('MIA', 'Miami Dolphins'),
                ('MIN', 'Minnesota Vikings'),
                ('NE', 'New England Patriots'),
                ('NO', 'New Orleans Saints'),
                ('NYG', 'New York Giants'),
                ('NYJ', 'New York Jets'),
                ('PHI', 'Philadelphia Eagles'),
                ('PIT', 'Pittsburgh Steelers'),
                ('SF', 'San Francisco 49ers'),
                ('SEA', 'Seattle Seahawks'),
                ('TB', 'Tampa Bay Buccaneers'),
                ('TEN', 'Tennessee Titans'),
                ('WAS', 'Washington Commanders')]

# team schedule search form
class TeamForm(FlaskForm):
    #teamName = StringField('Team', [DataRequired()]) # Open text field version of form
    teamName = SelectField('', [DataRequired()], choices=teamChoices) # drop down menu
        
    submit = SubmitField('Submit') # submit button

