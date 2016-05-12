import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import sys

np.random.seed(3)

def genData(fold):
    lines = open('features_'+fold, 'r').read().splitlines()
    
    if 'rep' in fold:
        num_cand = 4
        cands = [1, 2, 3, 4]
    else:
        num_cand = 2
        cands = [1, 2]

    features_X = []
    features_Y = []

    this_num = 0
    this_features = []
    this_ys = []
    for line in lines:
        this_line = line.split('\t')
        this_features += [float(x) for x in this_line[0].split(', ')]
        ys = this_line[1].split(', ')
        this_ys.append(int(ys[1]))
        this_num += 1
        if this_num == num_cand:
            this_num = 0
            features_Y.append(sum([a * b for a, b in zip(this_ys, cands)]))
            features_X.append(this_features)
            this_ys = []
            this_features = []

    rand_perm = np.random.permutation(len(features_Y))
    features_X = [features_X[i] for i in rand_perm]
    features_Y = [features_Y[i] for i in rand_perm]

    return [features_X, features_Y]

dem_data = genData('dem')
rep_data = genData('rep')

[train_X_rep, train_Y_rep] = [rep_data[0][0:32], rep_data[1][0:32]]
[validation_X_rep, validation_Y_rep] = [rep_data[0][33:37], rep_data[1][33:37]]
[test_X_rep, test_Y_rep] = [rep_data[0][37:], rep_data[1][37:]]

[train_X_dem, train_Y_dem] = [dem_data[0][0:31], dem_data[1][0:31]]
[validation_X_dem, validation_Y_dem] = [dem_data[0][32:36], dem_data[1][32:36]]
[test_X_dem, test_Y_dem] = [dem_data[0][36:], dem_data[1][36:]]

     
dem_persons = [ 'bernie_sanders', 'hillary_clinton'] 
rep_persons = ['donald_trump', 'marco_rubio',  'john_kasich','ted_cruz']
print "Republicans"
for i in range(5,6):
    clf = SVC(C = i, random_state = 1)
    clf.fit(train_X_rep, train_Y_rep)
    print "Accuracy = " + str(clf.score(test_X_rep, test_Y_rep))
    
    predictions = [rep_persons[i-1] for i in clf.predict(test_X_rep)]
    for index, y in enumerate(test_Y_rep):
        print ('-> Predicted: ' + predictions[index] + ', Actual: '  + str(rep_persons[y-1]) + ' ')
    print


print "Democrats"
for i in range(5, 6):
    clf = SVC(C = i, random_state = 1)
    clf.fit(train_X_dem, train_Y_dem)
    print "Accuracy = " + str(clf.score(test_X_dem, test_Y_dem))
    
    predictions = [dem_persons[i-1] for i in clf.predict(test_X_dem)]
    for index, y in enumerate(test_Y_dem):
        print ( '-> Predicted: ' + predictions[index] + ', Actual: '  + str(dem_persons[y-1]) + ' ')
    print
