import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import sys

to_predict_place = sys.argv[1] 

feature_days = 14 - int(sys.argv[2])

def genData(fold):
    lines = open('place_features_'+fold, 'r').read().splitlines()
    
    if 'rep' in fold:
        num_cand = 4
        cands = [1, 2, 3, 4]
    else:
        num_cand = 2
        cands = [1, 2]

    features_X_train = []
    features_Y_train = []

    features_X_test = []
    features_Y_test = []

    found = False

    this_num = 0
    this_features = []
    this_ys = []
    for line in lines:
        line = line.split('$')
        place = line[0].strip()
        line = line[1]
        this_line = line.split('\t')
        new_features = [float(x) for x in this_line[0].split(', ')]
        new_features = new_features[0:4]+ new_features[-feature_days*3:]

        this_features += new_features
        ys = this_line[1].split(', ')
        this_ys.append(int(ys[1]))
        this_num += 1
        if this_num == num_cand:
            this_num = 0
            if(place==to_predict_place):
                found = True
                features_Y_test.append(sum([a * b for a, b in zip(this_ys, cands)]))
                features_X_test.append(this_features)
            else:
                features_Y_train.append(sum([a * b for a, b in zip(this_ys, cands)]))
                features_X_train.append(this_features)

            this_ys = []
            this_features = []

    return [features_X_train, features_Y_train, features_X_test, features_Y_test, found]

dem_data = genData('dem')
rep_data = genData('rep')

[train_X_rep, train_Y_rep, test_X_rep, test_Y_rep, found_rep] = genData('rep')
[train_X_dem, train_Y_dem, test_X_dem, test_Y_dem, found_dem] = genData('dem')

dem_persons = [ 'bernie_sanders', 'hillary_clinton'] 
rep_persons = ['donald_trump', 'marco_rubio',  'john_kasich','ted_cruz']
dict_pred = {"rep": {"actual": "---", "predicted": "---"}, "dem": {"actual": "---", "predicted": "---"}}

if(found_rep): 
    for i in range(5,6):
        clf = SVC(C = i, random_state = 1)
        clf.fit(train_X_rep, train_Y_rep)
        predictions = [rep_persons[i-1] for i in clf.predict(test_X_rep)]
        answer = {}
        for index, y in enumerate(test_Y_rep):
            answer['predicted'] = predictions[index]
            answer['actual'] = str(rep_persons[y-1]) 
        dict_pred['rep'] = answer

if(found_dem):
    for i in range(5, 6):
        clf = SVC(C = i, random_state = 1)
        clf.fit(train_X_dem, train_Y_dem)
        predictions = [dem_persons[i-1] for i in clf.predict(test_X_dem)]
        answer = {}
        for index, y in enumerate(test_Y_dem):
            answer['predicted'] = predictions[index]
            answer['actual'] = str(dem_persons[y-1]) 
        dict_pred['dem'] = answer

print str(dict_pred).replace('\'', '\"')