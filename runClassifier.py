import pickle
import pandas as pd
import classifier1

class runClassifier:

    def __init__(self):
        classifiers = runClassifier.open_classifier()
        self.english_classifier = classifiers[0]
        self.arabic_classifier = classifiers[1]

    @staticmethod
    def open_classifier():

        # first classifier
        #with open('analyzer.pkl', 'rb') as analyzer_file:
        #    analyzer = pickle.load(analyzer_file)
        #with open('classifier.pkl', 'rb') as classifier_file:
        #    classifier = pickle.load(classifier_file)

        # open second classifier
        # english classifier
        with open('second_classifier_en.pkl', 'rb') as classifier_file:
            classifier2_en = pickle.load(classifier_file)
        # arabic classifier
        with open('second_classifier_ar.pkl', 'rb') as classifier_file:
            classifier2_ar = pickle.load(classifier_file)
        return [classifier2_en, classifier2_ar]

    #def assign_sentiment(tweet):
    #    test_set = analyzer.apply_features([(tweet['filtered_text'], '')])
    #    prob = classifier.prob_classify(test_set[0][0])
    #    return prob.prob('pos')
    
    def assign_sentiment2(self, tweet):
        test_set = classifier1.create_word_features(tweet['filtered_text'])
        if(tweet['lang'] == 'en'):
            prob = self.english_classifier.prob_classify(test_set)
        else:
            prob = self.arabic_classifier.prob_classify(test_set)
        return (prob.prob('positive')) 
    
    def analyse_tweets(self, df):
        #df['sentiment'] = df.apply(assign_sentiment, axis=1)
        df['sentiment2'] = df.apply(self.assign_sentiment2, axis=1)

if __name__ == "__main__":
    classify = runClassifier()
    df = pd.read_pickle('tweets.pkl')
    classify.analyse_tweets(df)
    df.to_pickle('tweets.pkl')
