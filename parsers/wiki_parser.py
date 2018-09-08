from bs4 import BeautifulSoup
from urllib.request import urlopen


def parse_year(year):
    r = urlopen('https://en.wikipedia.org/wiki/%s_FIFA_World_Cup_squads' % year).read()
    soup = BeautifulSoup(r, 'html.parser')

    country_info = {}
    tables = soup.select('table.wikitable')[:32]
    for table in tables:
        country = table.previous_sibling
        while country.name != 'h3':
            country = country.previous_sibling
        #country = table.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        #if year in ['2014', '2018']: country = country.previous_sibling.previous_sibling
        country = country.text
        print(country)
       # country = country[:-6]
        country = country.strip()
        country_info[country] = get_player_info(table, year)

    return country_info


def get_player_info(table, year):
    rows = table.select('tr')[1:]    
    a_list = []
    for player in rows:
        name = player.select('th')[0].text
        print(name, year)
        player_link = player.select('th a')[0]['href']
        season_stats = get_goals_apps(player_link, year)
        age = get_age(player.select('td')[2].text)
        caps = player.select('td')[3].text
        club_stats = player.select('td')[4]
        club = club_stats.text
        country = club_stats.select('span a')
        if country: country = country[0]['title']
        else: country = None
        dict = {
        'name': name, 
        'age': age,
        'caps': caps,
        'club': club,
        'country': country,
        'goals': season_stats[1],
        'apps': season_stats[0]
        }
        a_list.append(dict)
    return a_list


def get_age(wiki_info):
    age = wiki_info.split('(')[2]
    age = age.split(' ')[1]
    age = age[:-1]
    return age

def parse_years():
    info = {}
    for i in ['2014', '2010', '2006', '2002', '1998', '1994']:
        info[i] = parse_year(i)
    from utils import write_json
    write_json('/home/karol/python/predictor/data/team_info', info)

def add_year(year):
    from utils import read_json, write_json
    info = read_json('/home/karol/python/predictor/data/team_info')
    info[year] = parse_year(year)
    write_json('/home/karol/python/predictor/data/team_info', info)
    print('Done')


# tuple of goals, appearences
def get_goals_apps(player_link, year):
    r = urlopen('https://wikipedia.org' + player_link)
    soup = BeautifulSoup(r, 'html.parser')
    import utils

    stats = [0, 0]

    f_year = '%s–%s' % (str(int(year)-1), year[2:])
    print(f_year)
    table_rows = soup.select('#mw-content-text > .mw-parser-output > .wikitable')
    if not table_rows:
        print('Couldnt get info for this guy')
        return stats
    table_rows = table_rows[0].select('tr')

    for row in table_rows:
        data = row.select('td')
        if not data: continue
        if check_year(data, year):
            try:
                delimi = 0
                if not utils.is_a_number(data[len(data) -1].text): delimi = 1 
                stats[0] += int(data[len(data) -2 - delimi].text)
                stats[1] += int(data[len(data) -1 - delimi].text)
            except:
                print('Error getting stats', data)
    print (stats)
    return stats

def check_year(data, year):
    f_year = '%s–%s' % (str(int(year)-1), year[2:])
    prev_year = str(int(year)-1)

    counter = 3
    if len(data) < 3: counter = 2
    if len(data) < 2: counter = 1

    for i in range(counter):
        j = data[i].text
        p = j.split('[')[0]
        if p in [f_year, prev_year]:
            return True
    return False




'''
Gets info for year and country as dictionary
age: average age of squad
caps: average caps of squad
team: average number of players playing for the same team
country: average number of players playing in the same country
'''
def get_info(year, team):
    from parsers.utils import read_json, get_alternate_names
    data = read_json('/home/karol/python/predictor/data/team_info')
    year = data[year]
    t = team
    counter = 0
    k = get_alternate_names(t)
    while team not in year.keys():
        if counter < len(k):
            team = k[counter]
            counter += 1
        else:
            print(year.keys())
            team = input('%s couldn\'t be found. Please enter it in manually:\n' % t)
    country_info = year[team]
    dict_info = {
    'age': get_average_ints(country_info, 'age'),
    'caps': get_average_ints(country_info, 'caps'),
    'team': get_average_grouped(country_info, 'club'),
   # 'country': get_average_grouped(country_info, 'country'),
    'apps': get_average_ints(country_info, 'apps'),
    'goals': get_average_ints(country_info, 'goals'),
    #'g': max([int(x['goals']) for x in country_info])
    }
    return dict_info

def get_average_ints(data, key):
    l = [int(x[key]) for x in data if x[key] not in ['N/A', 'NA', '0']]
    if len(l) == 0: return 0
    return sum(l)//len(l)

def get_average_grouped(data, key):
    a_list = [x[key] for x in data]
    from collections import Counter
    r = Counter(a_list)
    return sum(r.values())//len(r)

