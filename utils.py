from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize 
from emoji import UNICODE_EMOJI
from nltk.sentiment.util import mark_negation
from unicodedata import category
from nltk.stem import PorterStemmer
import re
import farasa

from contractions import contractions

i = 1

arabic_stopword = ['في','من','علي' ,'على', 'أن', 'الى','التي', 'عن', 'لا','ما', 'او',
'هذا', 'هذه', 'الذي', 'كان', 'مع', 'و', 'ذلك', 'في', 'الله', 'بين', 'كل', 'هو',
'كما', 'لم', 'بعد', 'ان', 'ازاى', 'ليه', 'ازاي', 'عشان', 'علشان' ]

porter = PorterStemmer()

def process(tweet):
    global i
    print(i)
    i += 1

    text = tweet['text'].lower()
    lang = tweet['lang']
    try:
        mentions = tweet['mentions']
        urls = tweet['urls']
    except KeyError:
        mentions = []
        urls = []
    
    text = filter_tweet(text, mentions, urls)
    [text, emoji_text] = separate_emojis(text)

    if lang == 'ar':
        farasa.lemmatize(text)
        text = remove_arabic_variants(text)
        text = text + " " + " ".join(emoji_text)
    if(lang == 'en'):
        text = expand_contractions(text)
    text = remove_stopwords(text, lang)
    text = mark_negation(text)
    text = remove_punct(text)
    # old_text = text
    text = normalize_repititions(text, lang)
    if(lang == 'en'):
        text = stem_words(text)
    # if(old_text != text):
    #     print('old text: %s, new text: %s' %(tweet['text'], ' '.join(text)))
    print(text)
    return text

def remove_arabic_variants(text):
    variants = [('أ', 'ا'), ('آ', 'ا'), ('إ', 'ا'), ('ى', 'ي'), ('ة', 'ه')]
    for variant in variants:
        text = text.replace(variant[0], variant[1])
    return text

def separate_emojis(text):

    emoji_text = []
    for emoji in UNICODE_EMOJI.keys():
        last_index = 0
        while True:
            try:
                next_index = text.index(emoji, last_index)
                last_index = next_index + len(emoji) + 3
                text = text[0:next_index] + ' ' + emoji + ' ' + text[next_index+len(emoji):len(text)]
                emoji_text.append(emoji)
            except ValueError:
                break
    for emoji in emoji_text:
        text = text.replace(emoji, "")
    return [text, emoji_text]

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
    words = text.split()
    new_words = []
    for word in words:
        if word in contractions:
            new_words.append(contractions[word])
        else:
            new_words.append(word)
    return ' '.join(new_words).lower()

def remove_stopwords(text, lang):
    if(lang == 'en'):
        list = stopwords.words('english') + ['rt']
        for word in ['not', 'no']:
            list.remove(word)
    else:
        list = stopwords.words('arabic') + ['rt'] + arabic_stopword
        list += ['و' + x if not x.startswith('و') else x for x in list]
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

def normalize_repititions(text, lang):
    if lang == 'ar':
        text = [normalize_token_ar(token) for token in text]
    elif lang == 'en':
        text = [normalize_token_en(token) for token in text]
    
    return text

def normalize_token_ar(text):
    i = 1
    while i < len(text):
        if (text[i] == 'ا' or text[i] == ',') and text[i] == text[i-1]:
            text = text[0:i] + text[i+1:len(text)]
            i -= 1
        if text[i] == 'ي' and text[i] == text[i-1] and (i < len(text)-2 or not text.endswith('يين')):
            text = text[0:i] + text[i+1:len(text)]
            i -= 1
        i += 1
    return text

def normalize_token_en(text):
    while True:
        match = re.search('(\w)\\1{2,}', text)
        if match == None:
            break
        span = match.span()
        char = match.group(1)
        single = text[0:span[0]] + char + text[span[1]:len(text)]
        double = text[0:span[0]] + char + char + text[span[1]:len(text)]
        if double in words.words():
            text = double
        elif single in words.words():
            text = single
        else:
            if char in ['a', 'e', 'i', 'o', 'u']:
                text = double
            else:
                text = single

    return text

def stem_words(text):
    new_text = []
    for word in text:
        new_text.append(porter.stem(word))
    return new_text
