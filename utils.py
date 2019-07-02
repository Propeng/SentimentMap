def filter_tweet(tweet):
    text = tweet['text']
    for item in tweet['mentions'] + tweet['urls']:
        start = item['indices'][0]
        end = item['indices'][1]
        text = text[0:start] + ' '*(end-start) + text[end:len(text)]
    return ' '.join(text.split())