import pandas as pd

df = pd.read_pickle('tweets.pkl')

#Get average sentiment

sentiments = {}
for index, tweet in df.iterrows():
    region = tweet['region']
    sentiment = tweet['sentiment']

    try:
        sentiments[region].append(sentiment)
    except KeyError:
        sentiments[region] = []
        sentiments[region].append(sentiment)

print("Region averages")
avgs = {}
for region in sentiments.keys():
    avg = sum(sentiments[region]) / len(sentiments[region])
    avgs[region] = avg
    print(region, avg)
print()

#Get coord bounds

precise = []
for index, tweet in df.iterrows():
    if tweet['geo'] != None:
        precise.append(tweet)

print("Tweets with coords", len(precise))
print("All tweets", len(df['geo']))

min_lat = None
max_lat = None
min_long = None
max_long = None

for tweet in precise:
    coords = tweet['geo']['coordinates']
    if min_lat == None or coords[0] < min_lat:
        min_lat = coords[0]
    if max_lat == None or coords[0] > max_lat:
        max_lat = coords[0]
    if min_long == None or coords[1] < min_long:
        min_long = coords[1]
    if max_long == None or coords[1] > max_long:
        max_long = coords[1]

print("Min coords", min_lat, min_long)
print("Max coords", max_lat, max_long)

#Load plot arrays

plot_x = []
plot_y = []
plot_c = []

pos_color = (0,1,0)
neg_color = (1,0,0)

def sentiment_color(sentiment):
    return tuple(pos_color[i]*sentiment + neg_color[i]*(1-sentiment) for i in range(3))

for tweet in precise:
    coords = tweet['geo']['coordinates']
    sentiment = tweet['sentiment']

    plot_x.append(coords[1])
    plot_y.append(coords[0])
    
    color = sentiment_color(sentiment)
    plot_c.append(color)

#Plot map

import shapefile as shp
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import math
from regions import regions

fig, ax = plt.subplots(figsize=(10,10))

highway = gpd.read_file('egypt_highway')
highway.plot(ax=ax, linewidth=0.3, color=(0.7, 0.7, 0.7))

plt.scatter(plot_x, plot_y, s=10, c=plot_c)

for region in regions:
    geo = region['geocode'].split(',')
    
    lat = float(geo[0])
    lng = float(geo[1])
    radius = float(geo[2].strip("km"))
    radius_lat = radius / 110.574

    color = sentiment_color(avgs[region['name']])

    ax.add_artist(plt.Circle((lng, lat), radius_lat, color=color, fill=False, linewidth=2))

border = 0.01
plt.xlim(min_long-border, max_long+border)
plt.ylim(min_lat-border, max_lat+border)

plt.show()
