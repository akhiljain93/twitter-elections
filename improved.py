import datetime
import os
import sys

places = {}

features_dem = open('features_dem_' + sys.argv[1], 'w')
features_rep = open('features_rep_' + sys.argv[1], 'w')

demLines = open('democrats.csv', 'r').read().splitlines()
place_vote_share_dem = {}
for line in demLines:
    fields = line.strip().split(',')
    place = fields[1].lower().replace(' ', '').split('[')[0]
    if place not in place_vote_share_dem:
        place_vote_share_dem[place] = {}
    place_vote_share_dem[place]['hillary'] = float(fields[2].split('(')[1].split('%')[0])
    place_vote_share_dem[place]['bernie'] = float(fields[3].split('(')[1].split('%')[0])
    maxi = 0
    max_key = ''
    for key in place_vote_share_dem[place]:
        if place_vote_share_dem[place][key] > maxi:
            maxi = place_vote_share_dem[place][key]
            max_key = key
    place_vote_share_dem[place]['max'] = max_key

repLines = open('republicans.csv', 'r').read().splitlines()
place_vote_share_rep = {}
for line in repLines:
    fields = line.strip().split(',')
    place = fields[0].lower().replace(' ', '')
    if place not in place_vote_share_rep:
        place_vote_share_rep[place] = {}
    place_vote_share_rep[place]['donald'] = float(fields[1].split('%')[0])
    place_vote_share_rep[place]['ted'] = float(fields[2].split('%')[0])
    place_vote_share_rep[place]['kasich'] = float(fields[3].split('%')[0])
    place_vote_share_rep[place]['marco'] = float(fields[4].split('%')[0] if fields[4] is not '' else '0')
    maxi = 0
    max_key = ''
    for key in place_vote_share_rep[place]:
        if place_vote_share_rep[place][key] > maxi:
            maxi = place_vote_share_rep[place][key]
            max_key = key
    place_vote_share_rep[place]['max'] = max_key

democrats = ['hillary', 'bernie']

person_dates = {}

for directory in os.listdir('all_tweet_data_senti'):
    if directory not in person_dates:
        person_dates[directory.split('_')[0]] = {}
    for filename in os.listdir('all_tweet_data_senti/' + directory):
        count = [0., 0., 0.]
        for line in open('all_tweet_data_senti/' + directory + '/' + filename, 'r'):
            if line.strip() == '0':
                count[0] += 1
            if line.strip() == '2':
                count[1] += 1
            if line.strip() == '4':
                count[2] += 1
        total = sum(count)
        if total != 0:
            for i in range(len(count)):
                count[i] = count[i] / total
        person_dates[directory.split('_')[0]][datetime.datetime.strptime(filename, '%Y-%m-%d')] = count

primary_schedule = {'democrats': {}, 'republicans': {}}
for line in open('state_primary_schedule.csv', 'r').read().splitlines()[1:]:
    fields = line.strip().split(',')
    if fields[2] == '1':
        primary_schedule['democrats'][fields[0].lower().replace(' ', '')] = datetime.datetime.strptime(fields[1], '%Y-%m-%d')
    if fields[3] == '1':
        primary_schedule['republicans'][fields[0].lower().replace(' ', '')] = datetime.datetime.strptime(fields[1], '%Y-%m-%d')

for filename in os.listdir('data_senti/' + sys.argv[1]):
    fields = filename.strip().split('_')
    place = fields[0]
    count = [0., 0., 0.]
    for line in open('data_senti/' + sys.argv[1] + '/' + filename, 'r').read().splitlines():
        if line.strip() == '0':
            count[0] += 1
        if line.strip() == '2':
            count[1] += 1
        if line.strip() == '4':
            count[2] += 1
    total = sum(count)
    if total != 0:
        for i in range(len(count)):
            count[i] = count[i] / total
    this_features = count
    this_features.append(total)
    if fields[1] in democrats:
        this_date = primary_schedule['democrats'][place]
        for i in range(1, 15):
            from_date = this_date - datetime.timedelta(days = i)
            this_features += person_dates[fields[1]][from_date]
        features_dem.write(str(this_features)[1:-1])
        features_dem.write('\t')
        if fields[1] == place_vote_share_dem[place]['max']:
            features_dem.write(str(place_vote_share_dem[place][fields[1]]) + ', 1\n')
        else:
            features_dem.write(str(place_vote_share_dem[place][fields[1]]) + ', 0\n')
    else:
        this_date = primary_schedule['republicans'][place]
        for i in range(1, 15):
            from_date = this_date - datetime.timedelta(days = i)
            this_features += person_dates[fields[1]][from_date]
        features_rep.write(str(this_features)[1:-1])
        features_rep.write('\t')
        if fields[1] == place_vote_share_rep[place]['max']:
            features_rep.write(str(place_vote_share_rep[place][fields[1]]) + ', 1\n')
        else:
            features_rep.write(str(place_vote_share_rep[place][fields[1]]) + ', 0\n')

features_dem.close()
features_rep.close()
