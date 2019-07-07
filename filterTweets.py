import json
import os
import utils
import pandas as pd

tweets_dirs = ["./tweets/en/", "./tweets/ar/"]

files = []
for dir in tweets_dirs:
    files += [dir+filename for filename in os.listdir(dir)]

tweets = []
for filename in files:
    with open(filename, 'r') as json_file:
        tweets += json.loads(json_file.read())
        
df = pd.DataFrame(tweets)
df.set_index('id', drop = True, inplace=True)
print(df)

df['filtered_text'] = df.apply(utils.process, axis=1)

#temp['filtered2'] = df['filtered_text']

df.to_pickle("./tweets.pkl")

