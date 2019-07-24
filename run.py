import filterTweets
from runClassifier import runClassifier
import aggregate
import pandas as pd
from regions import regions
import datetime

def filter_and_classify(tweets):
    # preprocess tweets
    filterTweets.filter(tweets)
    
    # classify tweets
    classify = runClassifier()
    classify.analyse_tweets(tweets)

def plot(tweets, regions):
    # plot data
    aggregate.plot(tweets, regions)

def add_new_tweets(new_tweets):    
    df = pd.read_pickle('./tweets.pkl')
    df = df.append(new_tweets)
    df.to_pickle('./tweets.pkl')

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
    
    #load tweets
    tweets = filterTweets.load_files(dates, None)
    new_tweets = pd.DataFrame(tweets)
    new_tweets.set_index('id', drop = True, inplace=True)

    # preprocess and classify tweets
    filter_and_classify(new_tweets)

    # add new tweets to the pickle file
    add_new_tweets(new_tweets)
    
    # plot data
    plot(new_tweets, regions)

    return new_tweets

def classify_one(text, lang):
    
    # add tweet to data frame
    tweet = pd.DataFrame(list(zip([text], [lang])), 
               columns = ['text', 'lang']) 
    
    filter_and_classify(tweet)
    
    return tweet['sentiment2']


def classify_all():
    # load all tweets
    tweets_arr = filterTweets.load_files(None, None)
    tweets = pd.DataFrame(tweets_arr)
    tweets.set_index('id', drop = True, inplace=True)

    # filter and classify
    filter_and_classify(tweets)

    pd.to_pickle(tweets, 'tweets.pkl')
    return tweets


#dates = ["2019-07-16", "2019-07-20"]
#new_tweets = run_specific_date(dates)
#df = pd.read_pickle('./tweets.pkl')
#df2 = pd.read_pickle('./new_tweets_added.pkl')

#x = classify_one("RT @AssiellMustafa: +1 والله ، أنا بشكركوا جدا أنا من غيركو نثينج ربنا يخليكوا ليا 😂😂❤❤❤ https://t.co/m6AkXM0n6k", 'ar')

classify_all()
