
def get_team_names(deatils):
	outfile = open('team_names.txt', 'a+')

	teams = []
	for game in details:
		for i in ['home-team', 'away-team']:
			if game[i] not in teams:
				teams.append(game[i])

	outfile.write('\n'.join(teams))
	outfile.close()

def sort_team_names():
	file = open('team_names.txt', 'r')
	teams = file.read()
	teams = teams.split('\n')
	file.close()

	file = open('team_names.txt', 'w')
	for t in sorted(teams):
		file.write(t + '\n')
	file.close()


def parse_fixtures():
	file = open('fixtures_russia_2018.csv', 'r')
	details = []
	file.readline()

	for game in file:
		game = game.strip('\n')
		stuff = game.split(',')
		info = {
		'game': stuff[1],
		'date-time': stuff[2],
		'stage': stuff[3],
		'home-team': stuff[6],
		'away-team': stuff[7]
		}
		details.append(info)

	file.close()
	return details

def organize_matches():
	file = open('data/results.csv', 'r')
	r = file.readline()
	r = r.strip('\n')
	r = r.split(',')

	matches = []

	for stat in file:
		stat = stat.strip('\n')
		infos = stat.split(',')

		if infos[0] < "1985-01-01": continue
		k = {}
		for i, j in enumerate(r):
			k[j] = infos[i]
		matches.append(k)

	from parsers.utils import write_json
	write_json('data/matches', matches)

def get_wc_matches():
	from parsers import utils
	matches = utils.read_json('data/matches')
	wc_matches = []
	for match in matches:
		year = match['date'].split('-')[0]
		if year not in [str(x) for x in range(1990, 2019, 4)]: continue
		if match['tournament'] != 'FIFA World Cup': continue
		match_info = {
		'year': year, 
		'home_score': match['home_score'],
		'away_score': match['away_score'],
		'home_team': match['home_team'],
		'away-team': match['away_team'],
		'date': match['date'],
		'country': match['country']
		}
		wc_matches.append(match_info)
	utils.write_json('data/wc_matches', wc_matches)

def get_alternate_names():
	alternate_names = {}
	while True:
		former = input('Enter former name here: \n-> ')
		if former == 'no': break
		while True:
			latter = input('Enter a latter name here: \n-> ')
			if latter == 'no': break
			alternate_names[latter] = former
	from parsers.utils import write_json
	write_json('data/alternate_names', alternate_names)
'''
def compare(file1, file2):
	f1 = open(file1, 'r')
	f2 = open(file2, 'r')

	right_counter = 0
	wrong_lines = []
	for i in range(50):
		r1 = f1.readline()
		r2 = f2.readline()
		r1 = r1.strip('\n')
		r2 = r2.strip('\n')
		if r1[-1:] == r2[-1:]:
			right_counter += 1
		else:
			wrong_lines.append(i)
	print('Wrong lines are: %s\nAmount of wrongs is %i\n\nAmount of rights is %i\nWell Done!' % (str(wrong_lines), len(wrong_lines), right_counter))'''

def compare(f1, f2):
	file1 = open(f1, 'r')
	file2 = open(f2, 'r')

	file1.readline()
	file2.readline()

	right_results = 0
	right_scores = 0
	incorrect_teams = 0

	while True:
		r1 = file1.readline()
		r1 = r1.strip('\n')
		r2 = file2.readline()
		r2 = r2.strip('\n')

		if not r1 or not r2:
			break

		r1 = r1.split(',')
		r2 = r2.split(',')

		print(r1)
		print(r2)

		if r1[2] != r2[2] or r1[3] != r2[3]:
			incorrect_teams += 1
			continue

		if r1[4] == r2[4] and r1[5] == r2[5]:
			right_scores += 1
		if r1[6] == r2[6]:
			right_results += 1

	print ('Number of incorrect team predictions is %i\n\nNumber of right results is %i\n\nNumber of right scores is %i' 
		% (incorrect_teams, right_results, right_scores))


def cmp_line(file1, file2):
	f1 = open(file1, 'r')
	f2 = open(file2, 'r')

	while True:
		i = input()
		print(f1.readline(), end="")
		print(f2.readline(), end="")

compare('actual_brazil_2014.csv', 'predicted_brazil_5')
