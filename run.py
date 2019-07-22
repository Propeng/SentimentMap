import filterTweets
from runClassifier import runClassifier
import aggregate
import pandas as pd
from regions import regions
import datetime

# method to filter and plot data between 2 dates
def run_specific_date(dates):
    # dates is an array of start and end dates
    
    # extract all dates to analyse and plot
    [start_date, end_date] = dates
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    delta = end_date - start_date
    dates = []
    for i in range(delta.days +1):
        dates.append((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
    
    # preprocess tweets
    tweets = filterTweets.load_files(dates, None)
    new_tweets = pd.DataFrame(tweets)
    new_tweets.set_index('id', drop = True, inplace=True)
    filterTweets.filter(new_tweets)
    
    # classify tweets
    classify = runClassifier()
    classify.analyse_tweets(new_tweets)
    
    # add new tweets to the pickle file
    add_new_tweets(new_tweets)
    
    # plot data
    aggregate.plot(new_tweets, regions)
    return new_tweets
  
def classify_one(text, lang):
    
    # add tweet to data frame
    new_tweets = pd.DataFrame(list(zip([text], [lang])), 
               columns = ['text', 'lang']) 
    filterTweets.filter(new_tweets)
    
    # classify tweets
    classify = runClassifier()
    classify.analyse_tweets(new_tweets)
    
    return new_tweets['sentiment2']

def add_new_tweets(new_tweets):    
    df = pd.read_pickle('./tweets.pkl')
    df = df.append(new_tweets)
    df.to_pickle('./tweets.pkl')


#dates = ["2019-07-16", "2019-07-20"]
#new_tweets = run_specific_date(dates)
#df = pd.read_pickle('./tweets.pkl')
#df2 = pd.read_pickle('./new_tweets_added.pkl')

x = classify_one("RT @AssiellMustafa: +1 والله ، أنا بشكركوا جدا أنا من غيركو نثينج ربنا يخليكوا ليا 😂😂❤❤❤ https://t.co/m6AkXM0n6k", 'ar')
