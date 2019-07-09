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
import pickle
import utils


def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

if __name__ == "__main__":
    
    twitter_samples.fileids()
    
    strings = twitter_samples.strings('negative_tweets.json')
    i = 0
    neg_reviews = []
    for tweet in strings:
        tweet = tweet.replace(":", "").replace("(", "").replace(")", "")
        feature = create_word_features(utils.process({'text': tweet, 'lang': 'en'}))
        neg_reviews.append((feature, "negative"))
        print(i)
        i+=1
       
    strings = twitter_samples.strings('positive_tweets.json')   
    pos_reviews = []
    for tweet in strings:
        tweet = tweet.replace(":", "").replace("(", "").replace(")", "")
        feature = create_word_features(utils.process({'text': tweet, 'lang': 'en'}))
        pos_reviews.append((feature, "positive"))
        print(i)
        i+=1

#    print(len(neg_reviews))
#    print(len(pos_reviews))
#    print(neg_reviews[:5])
    


    arabic_neg = []
    arabic_pos = []
    lines = open('arabic_training.txt', 'r', encoding='utf-8').read().split('\n')
    for line in lines:
        fields = line.split('\t')
        if len(fields) >= 2:
            if fields[1] == "POS":
                feature = create_word_features(utils.process({'text': fields[0], 'lang': 'ar'}))
                arabic_pos.append((feature, 'positive'))
                print(i)
                i+=1
            elif fields[1] == "NEG":
                feature = create_word_features(utils.process({'text': fields[0], 'lang': 'ar'}))
                arabic_neg.append((feature, 'negative'))
                print(i)
                i+=1
        
#    print(len(arabic_neg))
#    print(len(arabic_pos))   
#    print(arabic_pos[:5])

    
    train_set_en = neg_reviews[:4000] + pos_reviews[:4000]
    test_set_en =  neg_reviews[0:1000] + pos_reviews[0:1000] 
    
    train_set_ar = arabic_neg[:int(len(arabic_neg)*0.8)] + arabic_pos[:int(len(arabic_pos)*0.8)]
    test_set_ar = arabic_neg[0:int(len(arabic_neg)*0.2)] + arabic_pos[0:int(len(arabic_pos)*0.2)]
    
#    print(len(train_set_en),  len(test_set_en))
    
    english_classifier = NaiveBayesClassifier.train(train_set_en)
    arabic_classifier = NaiveBayesClassifier.train(train_set_ar)
    
    accuracy_en = nltk.classify.util.accuracy(english_classifier, test_set_en)
    accuracy_ar = nltk.classify.util.accuracy(arabic_classifier, test_set_ar)
    print(accuracy_en)
    print(accuracy_ar)
    
    
#    for tweet in test_set_en:
#        print((tweet,english_classifier.classify(tweet[0])))
        
    with open('second_classifier_en.pkl', 'wb') as classifier_file:
        pickle.dump(english_classifier, classifier_file)
    with open('second_classifier_ar.pkl', 'wb') as classifier_file:
        pickle.dump(arabic_classifier, classifier_file)



