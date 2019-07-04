from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import extract_unigram_feats, mark_negation
import pandas as pd

import utils

df = pd.read_pickle('training.pkl')

pos_tweets = [(row['filtered_text'], 'pos') for index, row in df.loc[df['polarity'] == '4'].iterrows()]
neg_tweets = [(row['filtered_text'], 'neg') for index, row in df.loc[df['polarity'] == '0'].iterrows()]
all_tweets = pos_tweets + neg_tweets

analyzer = SentimentAnalyzer()
all_words = analyzer.all_words([mark_negation(doc) for doc in all_tweets])
unigram_feats = analyzer.unigram_word_feats(all_words, min_freq=4)
analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
training_set = analyzer.apply_features(all_tweets)
classifier = analyzer.train(NaiveBayesClassifier.train, training_set)

print('done')

while True:
    test_tweet = {'text': input()}
    utils.process(test_tweet)
    print(test_tweet['filtered_text'])
    test_set = analyzer.apply_features([(test_tweet['filtered_text'], '')])
    prob = classifier.prob_classify_many([doc[0] for doc in test_set])
    print("pos", prob[0].prob('pos'))
    print("neg", prob[0].prob('neg'))

