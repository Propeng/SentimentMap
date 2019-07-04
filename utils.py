from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from contractions import contractions

i = 1
def process(tweet):
    global i
    print(i)
    i += 1
    tweet['filtered_text'] = tweet['text']
    tweet['filtered_text'] = filter_tweet(tweet)
    tweet['filtered_text'] = expand_contractions(tweet)
    tweet['filtered_text'] = remove_stopwords(tweet)
    return tweet['filtered_text']

def filter_tweet(tweet):
    text = tweet['filtered_text']
    try:
        for item in tweet['mentions'] + tweet['urls']:
            start = item['indices'][0]
            end = item['indices'][1]
            text = text[0:start] + ' '*(end-start) + text[end:len(text)]
    except KeyError:
        pass

    #remove extra urls
    split = filter(lambda word: not word.startswith('http://') and not word.startswith('https://'), text.split())

    #remove mentions
    split = filter(lambda word: not word.startswith('@'), split)

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


