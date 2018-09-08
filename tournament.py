
class Tournament:

	def __init__(self):
		# Dictionary of games played, scored, conceded, gd, points
		self.tables = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}, 'G': {}, 'H':{}}
		self.groups_finished = False
		self.records = {}
		self.references = {}
		from parsers.utils import read_json
		self.r = read_json('/home/karol/python/predictor/data/matches')

	def update_match(self, group, home_team, away_team, home_score, away_score, game, result, date):
		self.r.append({
			"away_score": away_score,
	        "away_team": away_team,
	        "date": date,
	        "home_score": home_score,
	        "home_team": home_team
	    })
		if not self.groups_finished:
			self.update_group_match(group, home_team, away_team, home_score, away_score)
		else:
			if result == 'W':
				self.records['W'+game] = home_team
				self.records['L'+game] = away_team
			elif result == 'L':
				self.records['L'+game] = home_team
				self.records['W'+game] = away_team
			



	def get_reference(self, key):
		if key[:1] not in ['W', 'L']:
			return self.references[key]
		else:
			return self.records[key]



	def update_group_match(self, group, home_team, away_team, home_score, away_score):
		group = group.split(' ')[1]
		table = self.tables[group]

		home_score = int(home_score)
		away_score = int(away_score)

		home_points = 0
		away_points = 0
		if home_score > away_score:
			home_points = 3
			away_points = 0
		elif away_score > home_score:
			home_points = 0
			away_points = 3
		else:
			home_points = 1
			away_points = 1

		d = {
			home_team: [home_score, away_score, home_points],
			away_team: [away_score, home_score, away_points]
		}

		# Check if teams are present 
		for i in [home_team, away_team]:
			if i not in table:
				table[i] = [0, 0, 0, 0, 0, 0]
			table[i][0] += 1
			table[i][1] += d[i][0]
			table[i][2] += d[i][1]
			table[i][3] += d[i][0] - d[i][1]
			table[i][4] += d[i][2]
		self.tables[group] = table

		

		self.check_finished()

	def check_finished(self):
		for i in self.tables:
			table = self.tables[i]
			for j in table:
				team = table[j]
				if team[0] != 3:
					return
		self.groups_finished = True

		for i in self.tables:
			table = self.tables[i]
			print(table)
			table = self.sort_group(table)
			keys = list(table)
			one = ''
			two = ''
			for item in table:
				team = table[item]
				if team[5] == 1:
					one = item
				elif team[5] == 2:
					two = item
			self.references['1'+ i] = one
			self.references['2'+ i] = two

		from pprint import pprint
		pprint(self.tables)
		pprint(self.references)




	def sort_group(self, table):

		sorted = 1
		keys = list(table)
		print(table)
		for i in range(len(table)):

			highest = None
			highest_index = None

			for j in range(len(table)):
				current = table[keys[j]]
				print(current)
				if current[5] != 0:
					continue
				if highest_index == None and highest == None:
					highest_index = j
					highest = current

				if current[4] > highest[4] :
					current = highest
					highest_index = j
				elif current[4] == highest[4]:
					if current[3] > highest[3]:
						current = highest
						highest_index = j
					elif current[3] == highest[3]:
						if current[1] > highest[1]:
							current = highest
							highest_index = j

			print (keys[highest_index])
			table[keys[highest_index]][5] = sorted
			sorted += 1
		return table

	def get_form(self, country, date):
		from parsers.match_parser import get_form
		return get_form(country, date, self.r)

	def get_h2h(self, country1, country2, date):
		from parsers.match_parser import get_h2h
		return get_h2h(country1, country2, date, self.r)








