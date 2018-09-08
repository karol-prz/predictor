from bs4 import BeautifulSoup
from urllib.request import urlopen

#returns dictionary of countries and points
def get_page_rankings(url):
    r = urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    dict = {}
    table = soup.select('div.ranking04 > table > tbody > tr')
    for country in table:
        country = country.select('td')
        points = country[2].text
        nation = country[3].text
        nation = nation.strip()
        dict[nation] = points[:-3]
    return dict

# string year
def parse_year(year):
    url = 'http://en.fifaranking.net/ranking/?d=%s-04-28&rnkp=%s' % (year, '%s')
    dict = {}
    for i in range(1, 6):
        r = get_page_rankings(url % str(i))
        dict = {**dict, **r}
    return dict

def parse_years():
    rankings = {}
    for i in ['2018', '2014', '2010', '2006', '2002', '1998', '1994', '1990']:
        rankings[i] = parse_year(i)

    from parsers import utils
    utils.write_json('/home/karol/python/predictor/data/rankings', rankings)

def get_points(year, team):
    from parsers.utils import read_json, get_alternate_names
    rankings = read_json('/home/karol/python/predictor/data/rankings')
    year = rankings[year]
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
    return year[team]
'''
file = open('../team_names.txt', 'r')
for line in file:
    line = line.strip('\n')
    print(line)
    r = get_points('2014', line)
    print(r)

'''
