import json
import os
import utils
import pandas as pd
from regions import regions as all_regions

tweets_dirs = ["./tweets/en/", "./tweets/ar/"]

def filter(df):       
    df['filtered_text'] = df.apply(utils.process, axis=1)

def load_files(dates, regions):
    files = []
    if regions == None and dates == None:
        for dir in tweets_dirs:
            files += [dir+filename for filename in os.listdir(dir)]
    elif regions == None:
        regions = [region['name'] for region in all_regions]
        for region in regions:
            for date in dates:
                for dir in tweets_dirs:
                    files.append("%s%s_%s.json" %(dir, region, date))
        
    tweets = []
    for filename in files:
        with open(filename, 'r') as json_file:
            tweets += json.loads(json_file.read())
    return tweets
    
if __name__ == "__main__":
    tweets = load_files(None, None)
    df = pd.DataFrame(tweets)
    df.set_index('id', drop = True, inplace=True)
    print(df)
    filter(df)
    df.to_pickle("./tweets.pkl")
