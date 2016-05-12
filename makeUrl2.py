
import datetime
import os
import commands

def getSearchQuery(searchQuery):
    q = searchQuery.split(' ')
    ret = q[0]
    for token in q[1:]:
        ret = ret + '%20OR%20' + token
    return ret

def replaceSpaces(term):
    return term.replace(' ', '%20')

def getURL(searchQuery, to_date):
    to_date_time = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    to_date_time = to_date_time + datetime.timedelta(days=1)
    
    to_date = datetime.datetime.strftime(to_date_time, "%Y-%m-%d")
    from_date_time = to_date_time - datetime.timedelta(days=1)
    from_date = datetime.datetime.strftime(from_date_time, "%Y-%m-%d")
    
    url = 'https://twitter.com/search?q=' + getSearchQuery(searchQuery) + '%20lang%3Aen%20since%3A' + from_date + '%20until%3A' + to_date

    filename =  "all_tweet_data/" + searchQuery.replace(' ', '_') + "/" + from_date
    HA = commands.getstatusoutput("wc -l " + filename)
    lines = int(HA[1].split(' ')[0])
    cmd = "python selenium_parse.py " + url + " > " + filename
    if(lines==0):
        print cmd
        os.system(cmd)


democrat_list = ["hillary clinton", "bernie sanders"]
republican_list = ["ted cruz", "kasich", "donald trump", "marco rubio"]

#from 15Jan to 27April -> 104 days
from_index = 0
to_index = 104
start_date = '2016-01-15'
start_date_time = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=from_index)
curr_date_time = start_date_time
for i in range(0, to_index - from_index):
    curr_date_time = curr_date_time + datetime.timedelta(days=1)
    curr_date = datetime.datetime.strftime(curr_date_time, "%Y-%m-%d")
     
    for candidate in democrat_list:
        getURL(candidate, curr_date)
    for candidate in republican_list:
        getURL(candidate, curr_date)
    f = open('done_dates.txt', 'a+')
    f.write(curr_date + '\n')
    f.close()