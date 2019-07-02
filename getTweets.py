# Import the Twython class
from twython import Twython  
import json
import pandas as pd

regions = [('New Cairo', '29.988152,31.419053,10km')]

# Load credentials from json file
with open("credentials.json", "r") as file:  
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {'result_type': 'recent',
        'count': 100,
        'lang': 'en',
        }

# Search tweets
#dict_ = {'user': [], 'date': [], 'text': [], 'region': []}
tweets = []
for (region_name, geocode) in regions:
    query['geocode'] = geocode
    for status in python_tweets.search(**query)['statuses']:
        tweet = {}
        tweet['user'] = status['user']['screen_name']
        tweet['date'] = status['created_at']
        tweet['text'] = status['text']
        tweet['region'] = region_name
        tweets.append(tweet)

with open('tweets.json', 'w') as tweets_file:
    json.dump(tweets, tweets_file, indent=4)

# Structure data in a pandas DataFrame for easier manipulation
#df = pd.DataFrame(dict_)
#df.sort_values(by='favorite_count', inplace=True, ascending=False)
#df.head(5)
print('done')