from csv import reader
from re import sub
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import string

def uncliticise(tweet):
  tweet = sub(r"([A-Za-z]+)(n't)\b", '\g<1> not', tweet)
  tweet = sub(r"([A-Za-z]+)('s)\b", '\g<1> is', tweet)
  tweet = sub(r"([A-Za-z]+)('m)\b", '\g<1> am', tweet)
  tweet = sub(r"([A-Za-z]+)('re)\b", '\g<1> are', tweet)
  return tweet

def normalise(tweet):
  tweet = sub(r'(.)\1+', r'\1\1', tweet)
  return tweet

def remove_punctuations(tweet):
  tweet = tweet.translate(None, string.punctuation)
  return tweet

def unuser_and_unhashtag_and_unurl(tweet):
  tweet = sub(r"@\w+", "", tweet)
  tweet = sub(r"#(\w+)\b", '\g<1>', tweet)
  tweet = sub(r"(\w+:\/\/\S+)", "", tweet)
  return tweet

def remove_name(tweet):
  tweet.replace('donald trump', 'X')
  tweet.replace('hillary clinton', 'X')
  tweet.replace('bernie sanders', 'X')
  tweet.replace('trump', 'X')
  tweet.replace('donald', 'X')
  tweet.replace('hillary', 'X')
  tweet.replace('clinton', 'X')
  tweet.replace('bernie', 'X')
  tweet.replace('sanders', 'X')
  return tweet

def remove_tweets_with_two_people(tweet, filename):
  for person in people:
    if person not in filename and person in tweet:
      return ''
  return tweet

def preprocess(tweet, filename):
  tweet = tweet.strip().lower()
  tweet = remove_tweets_with_two_people(tweet, filename)

  if tweet == '':
    return tweet

  tweet = remove_name(tweet)
  tweet = uncliticise(tweet)
  tweet = unuser_and_unhashtag_and_unurl(tweet)
  tweet = remove_punctuations(tweet)
  tweet = normalise(tweet)
  return tweet

target = []
sentiment_target = []
files = ['bernie_sanders_train.txt', 'hillary_clinton_train.txt', 'donald_trump_train.txt']
people = ['donald', 'trump', 'hillary', 'clinton', 'bernie', 'sanders']

for filename in files:
    f = open(filename, 'rb')
    tweets = reader(f)
    for row in tweets:
      preprocessed_tweet = preprocess(row[1], filename)        
      if preprocessed_tweet is not '':
          target.append(preprocessed_tweet)
          sentiment_target.append(int(row[0]))
    f.close()

# Tokenise
vectorizer = TfidfVectorizer(decode_error = 'ignore', binary = True, ngram_range = (1, 2), min_df = 5, max_df = 0.3, norm = 'l2')

# Separtate 10% data as test set and 10% as dev set
X_train, X_test, y_train, y_test = train_test_split(target, sentiment_target, test_size = 0)

# Extract features from target set
features = vectorizer.fit_transform(X_train)

# Train source classifier
clf_source = joblib.load('best_source.pkl')
vectorizer_source = joblib.load('vectorizer_source.pkl')
prob_source = clf_source.predict_proba(vectorizer_source.transform(X_train))

# Train target classifier
clf_target = LogisticRegression(penalty = 'l2', C = 1.6, solver = 'lbfgs', multi_class = 'multinomial')
clf_target.fit(features, y_train)
prob_target = clf_target.predict_proba(features)

# Train merger classifier
clf = LogisticRegression(penalty = 'l2', C = 1.6, solver = 'lbfgs', multi_class = 'multinomial')
prob_final = []
for i in range(len(prob_source)):
  prob_final_i = []
  for j in range(len(prob_source[i])):
    prob_final_i.append(prob_source[i][j])
  for j in range(len(prob_target[i])):
    prob_final_i.append(prob_target[i][j])
  prob_final.append(prob_final_i)
clf.fit(prob_final, y_train)

joblib.dump(clf_source, '2011CS50274/best_source.pkl')
joblib.dump(clf_target, '2011CS50274/best_target.pkl')
joblib.dump(clf, '2011CS50274/best_merge.pkl')
joblib.dump(vectorizer_source, '2011CS50274/vectorizer_source.pkl')
joblib.dump(vectorizer, '2011CS50274/vectorizer_target.pkl')
