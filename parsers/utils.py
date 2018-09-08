def write_json(file, content):
    import json
    with open(file, 'w') as fp:
        json.dump(content, fp, sort_keys=True, indent=4)

def read_json(file):
    import json
    return json.load(open(file))

# Returns list of alternates
def get_alternate_names(country):
	r = get_alternate_ob(country)
	if r: return [country] + r
	else: return [country]  

def get_alternate_ob(country):
	r = read_json('/home/karol/python/predictor/data/alternate_names')
	i = {**r[0], **r[1]}
	try:
		k = i[country]
		if type(k) != type([]):
			j = get_alternate_ob(k)
			k = [k]
		else: 
			j = []
			for b in k: c = get_alternate_ob(b)
			if c: j.append(c)
		if j: return k + j
		else: return k
	except KeyError: return None

def parse_date(date):
	date = date[1:]
	date = date.split(' ')
	day = date[0]
	month = date[1]
	year = date[2]
	d = {'Jun': '06', 'Jul': '07'}
	month = d[month]
	return '%s-%s-%s' % (year, month, day)

def is_a_number(text):
	try:
		r = int(text)
		return True
	except ValueError:
		return False
