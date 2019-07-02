# Import the Twython class
from twython import Twython  
import json
import pandas as pd
from datetime import date, timedelta

regions = [
    {'name': 'New Cairo', 'geocode': '30.028652,31.465498,10km', 'tweets': []},
    {'name': 'Dokki', 'geocode': '30.039874,31.206894,3km', 'tweets': []},
    {'name': 'Heliopolis', 'geocode': '30.100987,31.342999,5km', 'tweets': []},
    {'name': 'Abbaseya', 'geocode': '30.065151,31.275649,3km', 'tweets': []},
]

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
for day_i in range(7):
    for region in regions:
        query['geocode'] = region['geocode']
        query['until'] = str(date.today() - timedelta(days=day_i))
        query['since'] = str(date.today() - timedelta(days=day_i+1))
        print(query)
        print()
        query_result = python_tweets.search(**query)

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
            tweet['region'] = region['name']
            region['tweets'].append(tweet)

# Write tweets to JSON files
for region in regions:
    print(region['name'], len(region['tweets']))
    with open('tweets/'+region['name']+'.json', 'w') as tweets_file:
        json.dump(region['tweets'], tweets_file, indent=4)

# Structure data in a pandas DataFrame for easier manipulation
#df = pd.DataFrame(dict_)
#df.sort_values(by='favorite_count', inplace=True, ascending=False)
#df.head(5)
print('done')