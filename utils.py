from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from contractions import contractions

def filter_tweet(tweet):
    text = tweet['text']
    for item in tweet['mentions'] + tweet['urls']:
        start = item['indices'][0]
        end = item['indices'][1]
        text = text[0:start] + ' '*(end-start) + text[end:len(text)]

    #remove extra urls
    split = filter(lambda word: not word.startswith('http://') and not word.startswith('https://'), text.split())

    #remove #'s at the beginning of hashtags
    split = map(lambda word: word.strip('#'), split)

    return ' '.join(split)

def expand_contractions(tweet):
    words = tweet['filtered_text'].lower().split()
    new_words = []
    for word in words:
        if word in contractions:
            new_words.append(contractions[word])
        else:
            new_words.append(word)
    return ' '.join(new_words).lower()

def remove_stopwords(tweet):
    stop_words = set(stopwords.words('english'))
    text = tweet['filtered_text']
    tokenized = word_tokenize(text)
    filtered_sentence = [w for w in tokenized if not w in stop_words] 
    return filtered_sentence


