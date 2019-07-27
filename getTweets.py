# Import the Twython class
from twython import Twython  
import json
import pandas as pd
from datetime import date, timedelta
from regions import regions

print("Tweets will be fetched for the days", str(date.today() - timedelta(days=7)),
    "to", str(date.today()))
print()

# Load credentials from json file
with open("credentials.json", "r") as file:  
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

def collect(days, languages):
    # Create our query
    for lang in languages:
        query = {'result_type': 'recent',
            'count': 100,
            'lang': lang,
            }

        # Search tweets
        #dict_ = {'user': [], 'date': [], 'text': [], 'region': []}
        for day_i in range(days):
            for region in regions:
                query['geocode'] = region['geocode']
                query['until'] = str(date.today() - timedelta(days=day_i))
                query['since'] = str(date.today() - timedelta(days=day_i+1))
                print(query)
                print()
                query_result = python_tweets.search(**query)
                print('Found %d tweets' %len(query_result['statuses']))
                for status in query_result['statuses']:
                    tweet = {}
                    tweet['id'] = status['id']
                    tweet['user'] = status['user']['screen_name']
                    tweet['user_location'] = status['user']['location']
                    tweet['date'] = status['created_at']
                    tweet['text'] = status['text']
                    tweet['geo'] = status['geo']
                    try:
                        tweet['bounding_box'] = status['bounding_box']
                    except KeyError:
                        pass
                    tweet['lang'] = status['lang']
                    tweet['urls'] = status['entities']['urls']
                    tweet['mentions'] = status['entities']['user_mentions']
                    #tweet['filtered_text'] = utils.filter_tweet(tweet)
                    #tweet['without_stopwords'] = utils.remove_stopwords(tweet)
                    tweet['region'] = region['name']
                    try:
                        region['tweets'][query['since']].append(tweet)
                    except KeyError:
                        region['tweets'][query['since']] = []
                        region['tweets'][query['since']].append(tweet)

        # Write tweets to JSON files
        for region in regions:
            for day in region['tweets'].keys():
                filename = region['name'] + '_' + day
                print(filename, len(region['tweets'][day]))
                with open('tweets/'+ lang + "/" +filename+'.json', 'w') as tweets_file:
                    json.dump(region['tweets'][day], tweets_file, indent=4)


if __name__ == "__main__":
    # Collect tweets from last 7 days
    days = 7
    languages = ['en', 'ar']
    collect(days, languages)
    
    # Structure data in a pandas DataFrame for easier manipulation
    #df = pd.DataFrame(dict_)
    #df.sort_values(by='favorite_count', inplace=True, ascending=False)
    #df.head(5)
    
    print('done')