from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import sys

def getFeatures(fold):
    lines = open('features_' + fold, 'r').read().splitlines()

    features_X = []
    features_Y = []

    if 'rep_' in fold:
        num_cand = 4
        cands = [1, 2, 3, 4]
    else:
        num_cand = 2
        cands = [1, 2]

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

    return [features_X, features_Y]

[train_X_rep, train_Y_rep] = getFeatures('rep_train')
[validation_X_rep, validation_Y_rep] = getFeatures('rep_validation')
[test_X_rep, test_Y_rep] = getFeatures('rep_test')

[train_X_dem, train_Y_dem] = getFeatures('dem_train')
[validation_X_dem, validation_Y_dem] = getFeatures('dem_validation')
[test_X_dem, test_Y_dem] = getFeatures('dem_test')

train_X_rep += validation_X_rep
train_Y_rep += validation_Y_rep
train_X_dem += validation_X_dem
train_Y_dem += validation_Y_dem

elections = ['Connecticut,2016-04-26', 'Delaware,2016-04-26', 'Maryland,2016-04-26', 'Pennsylvania,2016-04-26', 'Rhode Island,2016-04-26']
dem_persons = [ 'bernie_sanders', 'hillary_clinton'] 
rep_persons = ['donald_trump', 'marco_rubio',  'john_kasich','ted_cruz']
print "Republicans"
for i in range(10, 11):
        
    counts = [0, 0, 0, 0]
    for y in train_Y_rep:
        counts[int(y)-1]+=1
    maxv = -1
    maxi = -1
    for index, count in enumerate(counts):
        if(count>maxv):
            maxi = index+1
            maxv = count

    correct=0
    for y in test_Y_rep:
        if(y==maxi):
            correct+=1
        

    accuracy = (correct*1.0/len(test_Y_rep))


    print "Accuracy = " + str(accuracy)

    predictions = [rep_persons[maxi-1] for i in test_X_rep]
    for index, y in enumerate(test_Y_rep):
        print (elections[index] + ' -> Predicted: ' + predictions[index] + ', Actual: '  + str(rep_persons[y-1]) + ' ')
    print

print "\nDemocrats"
for i in range(35, 36):
    counts = [0, 0]
    for y in train_Y_dem:
        counts[int(y)-1]+=1
    maxv = -1
    maxi = -1
    for index, count in enumerate(counts):
        if(count>maxv):
            maxi = index+1
            maxv = count

    correct=0
    for y in test_Y_dem:
        if(y==maxi):
            correct+=1
                    
    accuracy = (correct*1.0/len(test_Y_dem))
    print "Accuracy = " + str(accuracy)
    
    predictions = [dem_persons[maxi-1] for i in test_X_dem]
    for index, y in enumerate(test_Y_dem):
        print (elections[index] + ' -> Predicted: ' + predictions[index] + ', Actual: '  + str(dem_persons[y-1]) + ' ')
    print
