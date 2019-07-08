from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from emoji import UNICODE_EMOJI
from nltk.sentiment.util import mark_negation
from unicodedata import category

from contractions import contractions

i = 1
#punct = '.,;():-\'"'  + '️' + '\u200d'  + '’'

def process(tweet):
    global i
    print(i)
    i += 1

    text = tweet['text']
    try:
        mentions = tweet['mentions']
        urls = tweet['urls']
    except KeyError:
        mentions = []
        urls = []

    text = filter_tweet(text, mentions, urls)
    text = separate_emojis(text)
    text = expand_contractions(text)
    text = remove_stopwords(text)
    text = mark_negation(text)
    text = remove_punct(text)
    return text

def separate_emojis(text):
    for emoji in UNICODE_EMOJI.keys():
        last_index = 0
        while True:
            try:
                next_index = text.index(emoji, last_index)
                last_index = next_index + len(emoji) + 3
                text = text[0:next_index] + ' ' + emoji + ' ' + text[next_index+len(emoji):len(text)]
            except ValueError:
                break
    
    return text

def filter_tweet(text, mentions, urls):
    for item in mentions + urls:
        start = item['indices'][0]
        end = item['indices'][1]
        text = text[0:start] + ' '*(end-start) + text[end:len(text)]

    #remove extra urls
    split = filter(lambda word: not word.startswith('http://') and not word.startswith('https://'), text.split())

    #remove mentions
    split = filter(lambda word: not word.startswith('@'), split)

    #remove #'s at the beginning of hashtags
    split = map(lambda word: word.strip('#'), split)

    return ' '.join(split)

def expand_contractions(text):
    words = text.lower().split()
    new_words = []
    for word in words:
        if word in contractions:
            new_words.append(contractions[word])
        else:
            new_words.append(word)
    return ' '.join(new_words).lower()

def remove_stopwords(text):
    list = (stopwords.words('english') + ['rt'])
    for word in ['not', 'no']:
        list.remove(word)
    stop_words = set(list)
    tokenized = word_tokenize(text)
    filtered_sentence = [w for w in tokenized if not w in stop_words] 
    return filtered_sentence

def remove_punct(text):
    filtered_text = []
    for word in text:
        original_word = word
        for c in word:
            if (category(c).startswith('P') or category(c) in ['Cf', 'Mn'] )and c not in ['?','!']:
                word = word.replace(c,'')

        # removing odd punctuation
        # Example: '...' or words ending in a punctuation symbol
        if(original_word.find(word) == -1):
            filtered_text.append(original_word)
        else:
            filtered_text.append(word)
    filtered_text = filter(lambda x: x != '' , filtered_text)
    return list(filtered_text)
