import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import sys

np.random.seed(1)

def genData(fold):
    lines = open('new_features_'+fold, 'r').read().splitlines()
    
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


rep_data_bucket_X = []
rep_data_bucket_Y = []

for i in range(0, len(rep_data[0])/4):
    bucket_X = []
    bucket_Y = []
    rng = 4
    if(i==9):
        rng = 5
    bucket_X = (rep_data[0][i*4:i*4+rng])
    bucket_Y = (rep_data[1][i*4:i*4+rng])
    rep_data_bucket_X.append(bucket_X)
    rep_data_bucket_Y.append(bucket_Y)

dem_data_bucket_X = []
dem_data_bucket_Y = []

for i in range(0, len(dem_data[0])/4):
    bucket_X = []
    bucket_Y = []
    rng = 4
    bucket_X = (dem_data[0][i*4:i*4+rng])
    bucket_Y = (dem_data[1][i*4:i*4+rng])
    dem_data_bucket_X.append(bucket_X)
    dem_data_bucket_Y.append(bucket_Y)
    
fres = open('new_rep_results.txt', 'w')
 
for c in range(6, 7):
    train_accuracy = []
    val_accuracy = []
    test_accuracy = []
    for i in range(0,10):
        validation_X_rep = rep_data_bucket_X[i]
        validation_Y_rep = rep_data_bucket_Y[i]
        train_X_rep = []
        train_Y_rep = []
        for k in range(0, 10):
            if(k==i):
                continue
            train_X_rep += rep_data_bucket_X[k]
            train_Y_rep += rep_data_bucket_Y[k]


        clf = SVC(C = c, random_state = 1)
        clf.fit(train_X_rep, train_Y_rep)
        predictions = clf.predict(validation_X_rep)
        correct=[]
        for indexx, y in enumerate(validation_Y_rep):
            fres.write(str(predictions[indexx]) + ',' + str(y) + '\n')
            if(y==predictions[indexx]):
                correct.append(1)
            else:
                correct.append(0)
                
        val_accuracy += correct
    fres.close()
    print 'Republicans 10 fold validation accuracy = ' + str(sum(val_accuracy)*100. / (len(val_accuracy) * 1.0))
fres = open('new_dem_results.txt', 'w')
for c in range(6, 7):
    train_accuracy = []
    val_accuracy = []
    test_accuracy = []
    for i in range(0,10):
        validation_X_dem = dem_data_bucket_X[i]
        validation_Y_dem = dem_data_bucket_Y[i]
        train_X_dem = []
        train_Y_dem = []
        for k in range(0, 10):
            if(k==i):
                continue
            train_X_dem += dem_data_bucket_X[k]
            train_Y_dem += dem_data_bucket_Y[k]
        clf = SVC(C = c, random_state = 1)
        clf.fit(train_X_dem, train_Y_dem)
        predictions = clf.predict(validation_X_dem)
        correct=[]
        for indexx, y in enumerate(validation_Y_dem):
            fres.write(str(predictions[indexx]) + ',' + str(y) + '\n')
            if(y==predictions[indexx]):
                correct.append(1)
            else:
                correct.append(0)
                
        val_accuracy += correct
    fres.close()
    print 'Democrats 10 fold validation accuracy = ' + str(sum(val_accuracy)*100. / (len(val_accuracy) * 1.0))
