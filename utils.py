from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def filter_tweet(tweet):
    text = tweet['text']
    for item in tweet['mentions'] + tweet['urls']:
        start = item['indices'][0]
        end = item['indices'][1]
        text = text[0:start] + ' '*(end-start) + text[end:len(text)]
    return ' '.join(text.split())

def remove_stopwords(tweet):
    stop_words = set(stopwords.words('english')) 
    text = tweet['filtered_text']
    tokenized = word_tokenize(text)
    filtered_sentence = [w for w in tokenized if not w in stop_words] 
    return filtered_sentence


    