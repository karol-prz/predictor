from parsers import utils, wiki_parser, world_rankings, match_parser
from tournament import Tournament
#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np

'''
x_values = {
	'h2h':
	'home_form':
	'away_form':
	'home_ranking':
	'away_ranking':
	'get_info(year, team).values()':
}
'''

def info(cache=True, use_cache=False):
	global tournament
	r = utils.read_json('data/wc_matches')
	info = []
	if use_cache:
		info = utils.read_json('data/cache')
		return info 

	for match in r:
		if match['year'] in ['1990']: continue
		print(match)
		info1 = {}
		h2h = tournament.get_h2h(match['home_team'], match['away-team'], match['date'])
		home_form = tournament.get_form(match['home_team'], match['date'])
		away_form = tournament.get_form(match['away-team'], match['date'])
		home_country = 1 if match['home_team'] == match['country'] else 0
		away_country = 1 if match['away-team'] == match['country'] else 0
		home_ranking = world_rankings.get_points(match['year'], match['home_team'])
		away_ranking = world_rankings.get_points(match['year'], match['away-team'])
		home_info = wiki_parser.get_info(match['year'], match['home_team']).values()
		away_info = wiki_parser.get_info(match['year'], match['away-team']).values()
		info1['x_values'] = [h2h, home_form, away_form, home_country, away_country, home_ranking, away_ranking] + list(home_info) + list(away_info)
		info1['y_values'] = [match_parser.get_result(utils.get_alternate_names(match['home_team']), match)]
		info1['x_values'] = [int(x) for x in info1['x_values']]
		info1['y_values'] = [int(x) for x in info1['y_values']]
		info1['home_score'] = [int(match['home_score'])]
		info1['away_score'] = [int(match['away_score'])]
		info.append(info1)

	if cache:
		utils.write_json('data/cache', info)

	return info

def fit(info):
	from pprint import pprint
	x = []
	y = []
	y_home = []
	y_away = []
	for i in info:
		#if (min(i['x_values'][-4:]) == 0):
		#	continue

		x.append(i['x_values'])
		y += i['y_values']
		y_home += i['home_score']
		y_away += i['away_score']

	x = np.array(x)

	y = np.array(y)
	y_home = np.array(y_home)
	y_away = np.array(y_away)

	global model_result, model_home, model_away

	# Train the model using the training sets 
	model_result.fit(x, y)
	model_home.fit(x, y_home)
	model_away.fit(x, y_away)
	

def predict(home_team, away_team, date, country):
	global model_result, model_home, model_away, year
	global home, away
	global tournament
	h2h = tournament.get_h2h(home_team, away_team, date)
	home_form = tournament.get_form(home_team, date)
	away_form = tournament.get_form(away_team, date)
	home_country = 1 if home_team == country else 0
	away_country = 1 if away_team == country else 0
	home_ranking = world_rankings.get_points(year, home_team)
	away_ranking = world_rankings.get_points(year, away_team)
	home_info = wiki_parser.get_info(year, home_team).values()
	away_info = wiki_parser.get_info(year, away_team).values()
	k = [h2h, home_form, away_form, home_country, away_country, home_ranking, away_ranking] + list(home_info) + list(away_info)
	k = [int(x) for x in k]

	home = model_home.predict(np.array([k]))
	away = model_away.predict(np.array([k]))

	r = model_result.predict(np.array([k]))
	if r == 1: return('W')
	elif r == 0: return('D')
	elif r == -1: return('L')
	else: return('Score is ' + str(r))


def process_file(file_name):
	file = open(file_name, 'r')
	global tournament, past_groups
	# Nr,Group,HomeTeam,AwayTeam,HomeScore,AwayScore,Wdl
	# Tournament,Game,DateTime,Group/Stage,Stadium,City,HomeTeam,AwayTeam

	file.readline()
	predictions = 'Nr,Group,HomeTeam,AwayTeam,HomeScore,AwayScore,Wdl\n'

	for line in file:
		line=line.strip('\n')
		stuff = line.split(',')
		home_team = stuff[len(stuff) - 2]
		if home_team == '1C': 
			past_groups = True
		away_team = stuff[len(stuff) - 1]
		if past_groups:
			home_team = tournament.get_reference(home_team)
			away_team = tournament.get_reference(away_team)
		date = utils.parse_date(stuff[2])
		country = stuff[0].split(' ')[0]
		result = predict(home_team, away_team, date, country)
		global home, away
		home = str(home)[1:-1]
		away = str(away)[1:-1]

		if home <= away and result == 'W':
			if home != away:
				home, away = away, home
			else:
				home = 2
				away = 1
		elif home >= away and result == 'L':
			if home != away:
				home, away = away, home
			else:
				home = 1
				away = 2
		elif result == 'D' and home != away and not past_groups:
			home = 1
			away = 1
		elif result == 'D' and past_groups:
			if home == away:
				home = 2
				away = 1
				result = 'W'
			elif home > away:
				result = 'W'
			else:
				result = 'L'
		
		d = [
			stuff[1],
			stuff[3],
			home_team,
			away_team,
			home,
			away,
			result
		]
		d = [str(x) for x in d]
		tournament.update_match(d[1], home_team, away_team, home, away, stuff[1], result, date)
		predictions += ','.join(d)+'\n'
		

	res = open('predicted_russia.csv', 'w')
	res.write(predictions)
		




#Create a Gaussian Classifier
model_result = GaussianNB()
model_home = GaussianNB()
model_away = GaussianNB()
tournament = Tournament()
year = '2018'
past_groups = False
fit(info(use_cache=False))
process_file('fixtures_russia_2018.csv')


