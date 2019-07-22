import math
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
from matplotlib.colors import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas as gpd
from shapely.geometry import Point, Polygon
from regions import regions

KM_PER_LAT = 110.574
pos_color = (0,1,0)
neg_color = (1,0,0)

# maps
highway = gpd.read_file('Shape Files/egypt_highway')
natural =  gpd.read_file('Shape Files/egypt_natural')
water = gpd.read_file('Shape Files/egypt_water')
coastline = gpd.read_file('Shape Files/egypt_coastline')
waterways_cairo = gpd.read_file("Shape Files/Kawkab el go3'rafya/planet_29.859,29.115_32.4,30.631-shp/shape/waterways.shp")

#Get average sentiment
def get_avg(df):
    sentiments = {}
    for index, tweet in df.iterrows():
        region = tweet['region']
        sentiment = tweet['sentiment2']

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
    return avgs

#Find tweets with geocode inside the region

def filter_precise_location(df):
    precise = []
    for index, tweet in df.iterrows():
        if tweet['geo'] != None:
            region = list(filter(lambda r: r['name'] == tweet['region'], regions))[0]

            coords = tweet['geo']['coordinates']
            lat = coords[0]
            lng = coords[1]

            geo = region['geocode'].split(',')
            region_lat = float(geo[0])
            region_long = float(geo[1])
            region_radius = float(geo[2].strip("km")) / KM_PER_LAT

            dist = math.sqrt((lat-region_lat)**2 + (lng-region_long)**2)

            if dist <= region_radius:
                precise.append(tweet)

    print("Tweets with coords", len(precise))
    print("All tweets", len(df['geo']))
    return precise

#Get plot bounds

def get_plot_bounds(regions): 
    min_lat = None
    max_lat = None
    min_long = None
    max_long = None

    for region in regions:
        geo = region['geocode'].split(',')
        region_lat = float(geo[0])
        region_long = float(geo[1])
        region_radius = float(geo[2].strip("km")) / KM_PER_LAT

        region_min_lat = region_lat-region_radius
        region_max_lat = region_lat+region_radius
        region_min_long = region_long-region_radius
        region_max_long = region_long+region_radius

        if min_lat == None or region_min_lat < min_lat:
            min_lat = region_min_lat
        if min_long == None or region_min_long < min_long:
            min_long = region_min_long
        if max_lat == None or region_max_lat > max_lat:
            max_lat = region_max_lat
        if max_long == None or region_max_long > max_long:
            max_long = region_max_long

    print("Min coords", min_lat, min_long)
    print("Max coords", max_lat, max_long)
    return [(min_lat, min_long), (max_lat, max_long)]

def sentiment_color(sentiment):
    return tuple(pos_color[i]*sentiment + neg_color[i]*(1-sentiment) for i in range(3))

def plot(new_tweets, regions):
    
    avgs = get_avg(new_tweets)
    precise = filter_precise_location(new_tweets)
    bounds = get_plot_bounds(regions)
    
    #Load plot arrays
    plot_x = []
    plot_y = []
    plot_c = []

    [(min_lat, min_long), (max_lat, max_long)] = bounds

    for tweet in precise:
        coords = tweet['geo']['coordinates']
        sentiment = tweet['sentiment2']

        plot_x.append(coords[1])
        plot_y.append(coords[0])
        
        #color = sentiment_color(sentiment)
        plot_c.append(sentiment)

    #Plot map

    fig, ax = plt.subplots(figsize=(10,10))

    highway.plot(ax=ax, linewidth=0.3, color=(0.7, 0.7, 0.7))
    natural.plot(ax = ax)
    water.plot(ax = ax)
    coastline.plot(ax = ax)
    waterways_cairo.plot(ax = ax)

    cmap = LinearSegmentedColormap.from_list('red-green', ['red', 'yellow', 'green'])
    plt.scatter(plot_x, plot_y, s=10, c=plot_c, cmap=cmap, vmin=0, vmax=1)

    for region in regions:
        geo = region['geocode'].split(',')
        
        lat = float(geo[0])
        lng = float(geo[1])
        radius = float(geo[2].strip("km"))
        radius_lat = radius / KM_PER_LAT

        color = cmap(avgs[region['name']])
        color = (color[0], color[1], color[2], 0.2)

        ax.add_artist(plt.Circle((lng, lat), radius_lat, color=color, linewidth=2))
        ax.text(lng, lat + radius_lat + 0.003, region['name'], horizontalalignment='center', verticalalignment='center',
            color=(0, 0, 0, 0.6), fontsize=14)

    border = 0.01

    plt.xlim(min_long-border, max_long+border)
    plt.ylim(min_lat-border, max_lat+border)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%', pad=0.05)
    cbar = plt.colorbar(cax=cax, ticks=[0, 0.5, 1])
    cbar.ax.set_yticklabels(['Negative', 'Neutral', 'Positive'])

    plt.show()

if __name__ == "__main__":
    df = pd.read_pickle('tweets.pkl')
    avgs = get_avg(df)
    precise = filter_precise_location(df)
    bounds = get_plot_bounds(regions)
    plot(avgs, precise, bounds)
