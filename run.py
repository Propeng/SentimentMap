import filterTweets
from runClassifier import runClassifier
import aggregate
import pandas as pd
from regions import regions as r
import datetime
from getTweets import collect
from datetime import date, timedelta
import datetime

regions = ["New Cairo", "Dokki", "Heliopolis", "Abbaseya"]

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

def extract_dates(dates):
     # extract all dates to analyse and plot
    [start_date, end_date] = dates
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    delta = end_date - start_date
    dates = []
    for i in range(delta.days +1):
        dates.append((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
    return dates

# classify new tweets between these dates
# tweets are loaded from json files
def run_specific_dates_from_json(dates):
    # dates is an array of start and end dates
    dates = extract_dates(dates)
   
    #load tweets
    tweets = filterTweets.load_files(dates, None)
    new_tweets = pd.DataFrame(tweets)
    new_tweets.set_index('id', drop = True, inplace=True)

    # preprocess and classify tweets
    filter_and_classify(new_tweets)
    
    # plot data
    plot(new_tweets, regions)

    return new_tweets

def classify_one(text, lang):
    
    # add tweet to data frame
    tweet = pd.DataFrame(list(zip([text], [lang])), 
               columns = ['text', 'lang']) 
    
    filter_and_classify(tweet)
    
    return tweet['sentiment2']

# classifies all tweets available in the json files
def classify_all():
    # load all tweets
    tweets_arr = filterTweets.load_files(None, None)
    tweets = pd.DataFrame(tweets_arr)
    tweets.set_index('id', drop = True, inplace=True)

    # filter and classify
    filter_and_classify(tweets)

    pd.to_pickle(tweets, 'tweets.pkl')
    return tweets

#Classify 1 tweet given the text and language
sentiment = classify_one(" والله ، أنا بشكركوا جدا أنا من غيركو نثينج ربنا يخليكوا ليا 😂😂❤❤❤", 'ar')

#To classify all tweets
tweets = classify_all()
#Plot all these tweets
plot(tweets, regions)

# collect tweets for the past num_days days in languages Arabic and English
num_days = 6
languages = ['en', 'ar']
collect(num_days, languages)
# filter and classify tweets
start_date = str(date.today() - timedelta(days=num_days))
end_date = str(date.today()- timedelta(days=1))
dates = [start_date, end_date]
new_tweets = run_specific_dates_from_json(dates)
regions = ["New Cairo", "Dokki", "Heliopolis", "Abbaseya"]
plot(new_tweets, regions)
# Add tweets to tweets.pkl
add_new_tweets(new_tweets)
df_old_plus_new = pd.read_pickle('./tweets.pkl')

# load classified data from the day 10/07/19 in new Cairo and plot it
dates = ["2019-07-10"]
specificRegions = ['New Cairo']
specific = filterTweets.load_data(dates, specificRegions )
plot(specific, specificRegions)
