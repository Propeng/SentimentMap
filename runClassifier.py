import pickle
import pandas as pd
import classifier1

# first classifier
with open('analyzer.pkl', 'rb') as analyzer_file:
    analyzer = pickle.load(analyzer_file)
with open('classifier.pkl', 'rb') as classifier_file:
    classifier = pickle.load(classifier_file)

# second classifier
with open('second_classifier.pkl', 'rb') as classifier_file:
    classifier2 = pickle.load(classifier_file)

def assign_sentiment(tweet):
    test_set = analyzer.apply_features([(tweet['filtered_text'], '')])
    prob = classifier.prob_classify(test_set[0][0])
    return prob.prob('pos')

def assign_sentiment2(tweet):
    test_set = classifier1.create_word_features(tweet['filtered_text'])
    prob = classifier2.prob_classify(test_set)
    return (prob.prob('positive')) 

df = pd.read_pickle('tweets.pkl')
df['sentiment'] = df.apply(assign_sentiment, axis=1)
df['sentiment2'] = df.apply(assign_sentiment2, axis=1)

df.to_pickle('tweets.pkl')


