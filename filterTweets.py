import json
import os
import utils
import pandas as pd
from regions import regions as all_regions
import datetime

tweets_dirs = ["./tweets/en/", "./tweets/ar/"]

def filter(df):       
    df['filtered_text'] = df.apply(utils.process, axis=1)

# load from json files if date is specified or nothing is specified
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
  
    
def load_data(dates, regions):
    tweets = pd.read_pickle('tweets.pkl')
    
    if regions:
        region_cond = tweets['region'].isin(regions)
    if dates:  
        date_cond = (tweets['date'].apply(lambda d: datetime.datetime.strptime(d, '%a %b %d %H:%M:%S %z %Y' ).strftime("%Y-%m-%d"))).isin(dates)
    if regions == None and dates == None:
        return tweets
    elif(dates == None):
        return tweets[region_cond]
    elif(regions == None):
        return tweets[date_cond] 
    
    cond = region_cond & date_cond
    return tweets[cond]

if __name__ == "__main__":
    tweets = load_files(None, None)
    df = pd.DataFrame(tweets)
    df.set_index('id', drop = True, inplace=True)
    print(df)
    filter(df)
    df.to_pickle("./tweets.pkl")

