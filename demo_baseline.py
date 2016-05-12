import sys
import numpy as np
fLines = open('baseline_counts.txt', 'r').read().splitlines()

places = {}


for line in fLines[:-1]:
    fields = line.strip().split(' ')
    count = float(fields[0])
    file_name = fields[1]
    place = file_name.split('_')[0]
    person = '_'.join(file_name.split('_')[1:])
    if place not in places:
        places[place] = {}
    places[place][person] = count

demLines = open('democrats.csv', 'r').read().splitlines()
place_vote_share_dem = {}
for line in demLines:
    fields = line.strip().split(',')
    place = fields[1].lower().replace(' ', '').split('[')[0]
    if place not in place_vote_share_dem:
        place_vote_share_dem[place] = {}
    if place not in places:
        print place
    place_vote_share_dem[place]['hillary_clinton'] = float(fields[2].split('(')[1].split('%')[0])
    place_vote_share_dem[place]['bernie_sanders'] = float(fields[3].split('(')[1].split('%')[0])

repLines = open('republicans.csv', 'r').read().splitlines()
place_vote_share_rep = {}
for line in repLines:
    fields = line.strip().split(',')
    place = fields[0].lower().replace(' ', '')
    if place not in place_vote_share_rep:
        place_vote_share_rep[place] = {}
    if place not in places:
        print place
    place_vote_share_rep[place]['donald_trump'] = float(fields[1].split('%')[0])
    place_vote_share_rep[place]['ted_cruz'] = float(fields[2].split('%')[0])
    place_vote_share_rep[place]['marco_rubio'] = float(fields[3].split('%')[0] if fields[3] is not '' else '0')
    place_vote_share_rep[place]['kasich'] = float(fields[4].split('%')[0] if fields[4] is not '' else '0')

f = open('vote_share_baseline.csv', 'w')
g = open('winners_baseline.csv', 'w')

correct = 0
wrong = 0
correct_dem = 0
wrong_dem = 0
correct_rep = 0
wrong_rep = 0
tot_mae = 0
tot_mae_count = 0

dem_persons = ['hillary_clinton', 'bernie_sanders'] 
rep_persons = ['donald_trump', 'ted_cruz',  'kasich', 'marco_rubio']
fres_rep = open('baseline_rep_results.txt', 'w')
fres_dem = open('baseline_dem_results.txt', 'w')
for place in places:
    if(place != sys.argv[1]):
        continue
    f.write(place)
    g.write(place)

    mae = 0
    mae_count = 0
    dict_pred = {"rep": {"actual": "---", "predicted": "---"}, "dem": {"actual": "---", "predicted": "---"}}
    if place in place_vote_share_dem:
        tot_tweets = 0
        tot_votes = 0
        max_tweets = -1
        max_tweets_person = ''
        max_votes = -1
        max_votes_person = ''
        for person in place_vote_share_dem[place]:
            tot_tweets += places[place][person]
            tot_votes += place_vote_share_dem[place][person]

            if max_votes < place_vote_share_dem[place][person]:
                max_votes = place_vote_share_dem[place][person]
                max_votes_person = person

            if max_tweets < places[place][person]:
                max_tweets = places[place][person]
                max_tweets_person = person

        if tot_tweets != 0:
            g.write(',' + max_tweets_person + ',' + max_votes_person)
            answer = {}
            answer['predicted'] = max_tweets_person
            answer['actual'] = max_votes_person
            dict_pred['dem'] = answer
            fres_dem.write(str((max_tweets_person)) + ',' + str((max_votes_person)) + '\n')

            if max_tweets_person == max_votes_person:
                correct += 1
                correct_dem += 1
            else:
                wrong += 1
                wrong_dem += 1

            for person in place_vote_share_dem[place]:
                places[place][person] /= tot_tweets

            if tot_votes != 0:
                for person in place_vote_share_dem[place]:
                    place_vote_share_dem[place][person] /= tot_votes
                    mae += abs(place_vote_share_dem[place][person] - places[place][person])
                    mae_count += 1

            for person in place_vote_share_dem[place]:
                f.write(',' + str(100 * places[place][person]) + ',' + str(100 * place_vote_share_dem[place][person]))
        else:
            max_tweets_person = dem_persons[np.random.randint(2)]
            g.write(',' + max_tweets_person + ',' + max_votes_person)
            answer = {}
            answer['predicted'] = max_tweets_person
            answer['actual'] = max_votes_person
            dict_pred['dem'] = answer
            fres_dem.write(str((max_tweets_person)) + ',' + str((max_votes_person)) + '\n')
            
            if max_tweets_person == max_votes_person:
                correct += 1
                correct_dem += 1
            else:
                wrong += 1
                wrong_dem += 1
            
            for person in place_vote_share_dem[place]:
                if(person==max_tweets_person):
                    f.write(',' + str(100) + ',' + str(100 * place_vote_share_dem[place][person]))
                else:
                    f.write(',' + str(100 * places[place][person]) + ',' + str(100 * place_vote_share_dem[place][person]))
                    
            g.write(',,')
    else:
        f.write(',,,,')
        g.write(',,')

    if place in place_vote_share_rep:
        tot_tweets = 0
        tot_votes = 0
        max_tweets = -1
        max_tweets_person = ''
        max_votes = -1
        max_votes_person = ''
        for person in place_vote_share_rep[place]:
            tot_tweets += places[place][person]
            tot_votes += place_vote_share_rep[place][person]

            if max_votes < place_vote_share_rep[place][person]:
                max_votes = place_vote_share_rep[place][person]
                max_votes_person = person

            if max_tweets < places[place][person]:
                max_tweets = places[place][person]
                max_tweets_person = person

        if tot_tweets != 0:
            g.write(',' + max_tweets_person + ',' + max_votes_person)
            answer = {}
            answer['predicted'] = max_tweets_person
            answer['actual'] = max_votes_person
            dict_pred['rep'] = answer
            fres_rep.write(str((max_tweets_person)) + ',' + str((max_votes_person)) + '\n')

            if max_tweets_person == max_votes_person:
                correct += 1
                correct_rep += 1
            else:
                wrong += 1
                wrong_rep += 1

            for person in place_vote_share_rep[place]:
                places[place][person] /= tot_tweets

            if tot_votes != 0:
                for person in place_vote_share_rep[place]:
                    place_vote_share_rep[place][person] /= tot_votes
                    mae += abs(place_vote_share_rep[place][person] - places[place][person])
                    mae_count += 1

            for person in place_vote_share_rep[place]:
                f.write(',' + str(100 * places[place][person]) + ',' + str(100 * place_vote_share_rep[place][person]))

        else:
            max_tweets_person = rep_persons[np.random.randint(2)]
            g.write(',' + max_tweets_person + ',' + max_votes_person)
            answer = {}
            answer['predicted'] = max_tweets_person
            answer['actual'] = max_votes_person
            dict_pred['rep'] = answer
            fres_rep.write(str((max_tweets_person)) + ',' + str((max_votes_person)) + '\n')
            
            if max_tweets_person == max_votes_person:
                correct += 1
                correct_rep += 1
            else:
                wrong += 1
                wrong_rep += 1
            
            for person in place_vote_share_rep[place]:
                if(person==max_tweets_person):
                    f.write(',' + str(100) + ',' + str(100 * place_vote_share_rep[place][person]))
                else:
                    f.write(',' + str(100 * places[place][person]) + ',' + str(100 * place_vote_share_rep[place][person]))
                    
            g.write(',,')
    else:
        f.write(',,,,,,,,')
        g.write(',,')

    if mae_count == 0:
        f.write(',')
    else:
        mae = 100 * mae / mae_count
        f.write(',' + str(mae))
        tot_mae += mae
        tot_mae_count += 1

    f.write('\n')
    g.write('\n')
    print str(dict_pred).replace('\'', '\"')

f.close()
g.close()
fres_rep.close()
fres_dem.close()
