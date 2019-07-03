import json
import os
import utils

tweets_dir = "./tweets/"

files = [tweets_dir+filename for filename in os.listdir(tweets_dir)]

for filename in files:
    with open(filename, 'r') as json_file:
        tweets = json.loads(json_file.read())
        
        for tweet in tweets:
            tweet['filtered_text'] = utils.filter_tweet(tweet)
            tweet['without_stopwords'] = utils.remove_stopwords(tweet)
        
        print(tweets)