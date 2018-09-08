from parsers import utils

def get_form(country, date, r):
	c_names = utils.get_alternate_names(country)
	#r = utils.read_json('/home/karol/python/predictor/data/matches')
	matches = []
	for i in r:
		if i['date'] < date and (i['home_team'] in c_names or i['away_team'] in c_names):
			matches.append(i)
	from operator import itemgetter
	newlist = sorted(matches, key=itemgetter('date'))
	newlist = newlist[:5]
	return sum([get_result(c_names, x) for x in newlist])

# returns cuntry1 h2h 
def get_h2h(country1, country2, date, r):
	c1_names = utils.get_alternate_names(country1)
	c2_names = utils.get_alternate_names(country2)
	#r = utils.read_json('/home/karol/python/predictor/data/matches')
	matches = []
	for i in r:
		if i['date'] < date and (i['home_team'] in c1_names or i['away_team'] in c1_names) and (i['home_team'] in c2_names or i['away_team'] in c2_names):
			matches.append(i)
	from operator import itemgetter
	newlist = sorted(matches, key=itemgetter('date'))
	newlist = newlist[:5]
	return sum([get_result(c1_names, x) for x in newlist])

# -1 for loss, 0 for draw, 1 for win
def get_result(country_names, match):
	result = 0
	if match['home_score'] < match['away_score']:
		if match['home_team'] in country_names:
			result = -1
	elif match['home_score'] == match['away_score']:
		result = 0
	else:
		result = 1
	return result