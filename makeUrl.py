import datetime
import os

def getSearchQuery(searchQuery):
    q = searchQuery.split(' ')
    ret = q[0]
    for token in q[1:]:
        ret = ret + '%20OR%20' + token
    return ret

def replaceSpaces(term):
    return term.replace(' ', '%20')

def getURL(searchQuery, to_date, lati, longi, place):
    radius = '100km'
    to_date_time = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    to_date_time = to_date_time - datetime.timedelta(days=1)
    
    to_date = datetime.datetime.strftime(to_date_time, "%Y-%m-%d")
    from_date_time = to_date_time - datetime.timedelta(days=14)
    from_date = datetime.datetime.strftime(from_date_time, "%Y-%m-%d")
    
    url = 'https://twitter.com/search?q=' + getSearchQuery(searchQuery) + '%20lang%3Aen%20near%3A%22' + lati + '%2C' + longi + '%22%20within%3A' + radius + '%20since%3A' + from_date + '%20until%3A' + to_date

    print url

    cmd = "python selenium_parse.py " + url + " > data/" + place.lower().replace(' ', '')   + "_" + searchQuery.replace(' ', '_') 
    print cmd
    os.system(cmd)


democrat_list = ["hillary clinton", "bernie sanders"]
republican_list = ["ted cruz", "kasich", "donald trump", "marco rubio"]

f = open('coordinates.csv', 'r')
coord_dict = {}
for line in f:
    line = line.strip()
    line = line.split(',')
    coord_dict[line[0]] = (line[1], line[2])

f = open('state_primary_schedule.csv', 'r')
f.readline()
for line in f:
    line = line.strip().split(',')
    if(line[2] == '1'):
        for candidate in democrat_list:
            getURL(candidate, line[1], coord_dict[line[0]][0], coord_dict[line[0]][1], line[0])
    if(line[3] == '1'):
        for candidate in republican_list:
            getURL(candidate, line[1], coord_dict[line[0]][0], coord_dict[line[0]][1], line[0])
