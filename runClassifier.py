import pickle
import pandas as pd

with open('analyzer.pkl', 'rb') as analyzer_file:
    analyzer = pickle.load(analyzer_file)
with open('classifier.pkl', 'rb') as classifier_file:
    classifier = pickle.load(classifier_file)

def assign_sentiment(tweet):
    test_set = analyzer.apply_features([(tweet['filtered_text'], '')])
    prob = classifier.prob_classify(test_set[0][0])
    return prob.prob('pos')

df = pd.read_pickle('tweets.pkl')
df['sentiment'] = df.apply(assign_sentiment, axis=1)

df.to_pickle('tweets.pkl')