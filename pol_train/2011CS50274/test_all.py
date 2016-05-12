import os
from re import sub
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import string
import sys

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

def preprocess(tweet):
  tweet = tweet.strip().lower()
  tweet = remove_name(tweet)
  tweet = uncliticise(tweet)
  tweet = unuser_and_unhashtag_and_unurl(tweet)
  tweet = remove_punctuations(tweet)
  tweet = normalise(tweet)
  return tweet

clf_source = joblib.load('best_source.pkl')
clf_target = joblib.load('best_target.pkl')
clf = joblib.load('best_merge.pkl')
vectorizer_source = joblib.load('vectorizer_source.pkl')
vectorizer_target = joblib.load('vectorizer_target.pkl')
for directory in os.listdir('../../all_tweet_data'):
    for filename in os.listdir('../../all_tweet_data/' + directory):
      f = open('../../all_tweet_data/' + directory + '/' + filename, 'r')
      tweets = []
      for line in f:
        tweets.append(preprocess(line))
      f.close()

      if len(tweets) == 0:
        continue

      prob_source = clf_source.predict_proba(vectorizer_source.transform(tweets))
      prob_target = clf_target.predict_proba(vectorizer_target.transform(tweets))
      prob_final = []
      for i in range(len(prob_source)):
        prob_final_i = []
        for j in range(len(prob_source[i])):
          prob_final_i.append(prob_source[i][j])
        for j in range(len(prob_target[i])):
          prob_final_i.append(prob_target[i][j])
        prob_final.append(prob_final_i)
      
      predictions = clf.predict(prob_final)
      
      f = open('../../all_tweet_data_senti/' + directory + '/' + filename, 'w')
      f.write('')
      for prediction in predictions:
        f.write(str(prediction) + '\n')
      f.write('\n')
      f.close()
