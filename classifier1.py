# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:23:33 2019

@author: lujine
"""
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

twitter_samples.fileids()
 
def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

create_word_features(["the", "quick", "brown", "fox", "fox"])

strings = twitter_samples.strings('negative_tweets.json')
neg_reviews = []
for tweet in strings:
    tweet = tweet.replace(":", "").replace("(", "").replace(")", "")
    feature = create_word_features(word_tokenize(tweet))
    print(feature)
    neg_reviews.append((feature, "negative"))
   
strings = twitter_samples.strings('positive_tweets.json')   
pos_reviews = []
for tweet in strings:
    tweet = tweet.replace(":", "").replace("(", "").replace(")", "")
    feature = create_word_features(word_tokenize(tweet))
    print(feature)
    pos_reviews.append((feature, "positive"))
    
print(len(neg_reviews))
print(len(pos_reviews))
print(neg_reviews[:5])

train_set = neg_reviews[:4000] + pos_reviews[:4000]
test_set =  neg_reviews[0:1000] + pos_reviews[0:1000]
print(len(train_set),  len(test_set))



classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.util.accuracy(classifier, test_set)

print(accuracy)


