import json
import os
import utils
import pandas as pd

tweets_dir = "./tweets/"

files = [tweets_dir+filename for filename in os.listdir(tweets_dir)]

tweets = []
for filename in files:
    with open(filename, 'r') as json_file:
        tweets += json.loads(json_file.read())
        
df = pd.DataFrame(tweets)
df.set_index('id', drop = True, inplace=True)
print(df)

df['filtered_text'] = df.apply(utils.process, axis=1)
#df['filtered_text'] = df['text']
#df['filtered_text'] = df.apply(utils.filter_tweet, axis=1)
#df['filtered_text'] = df.apply(utils.remove_stopwords, axis=1)

df.to_pickle("./tweets.pkl")

