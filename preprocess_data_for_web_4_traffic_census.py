"""
d:
cd D:\2020\coding\dashboard_demos
dashboard_env\Scripts\activate.bat
python
"""

import pandas as pd
import time
import sqlite3
from sqlite3 import Error
import json
from json import JSONEncoder
import numpy as np
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, acos, sqrt, pi

input_fn_trafficcensus2020 = "data/trafficcensus2020.csv"
df_traffic_census_2020 = pd.read_csv(input_fn_trafficcensus2020)
print("startup : df_traffic_census_2020.shape:", df_traffic_census_2020.shape)
df_traffic_census_2020.columns

list(df_traffic_census_2020.columns)
"""
['SITE', 'DESCRIPTION', 'LONGITUDE', 'LATITUDE', 'THROUGH_DISTANCE',
'ROAD_SECTION_ID', 'ROAD_NAME', 'THROUGH_DISTANCE_START', 'THROUGH_DISTANCE_END',
'AADT', 'PC_CLASS_0A', 'PC_CLASS_0B', 'PC_CLASS_1A', 'PC_CLASS_1B', 'PC_CLASS_1C',
'PC_CLASS_1D', 'GROWTH_PC_1YR', 'GROWTH_PC_5YR', 'GROWTH_PC_10YR', 'PC_CLASS_2A',
'PC_CLASS_2B', 'PC_CLASS_2C', 'PC_CLASS_2D', 'PC_CLASS_2E', 'PC_CLASS_2F',
'PC_CLASS_2G', 'PC_CLASS_2H', 'PC_CLASS_2I', 'PC_CLASS_2J', 'PC_CLASS_2K',
'PC_CLASS_2L', 'REPORT_LINK']
"""


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    All args must be of equal length.
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def calculate_spherical_distance(lon1, lat1, lon2, lat2):
    # from https://towardsdatascience.com/finding-distance-between-two-latitudes-and-longitudes-in-python-43e92d6829ff
    # https://en.wikipedia.org/wiki/Haversine_formula
    r=6371
    # Convert degrees to radians
    coordinates = lat1, lon1, lat2, lon2
    # radians(c) is same as c*pi/180
    phi1, lambda1, phi2, lambda2 = [
        radians(c) for c in coordinates
    ]
    # Apply the haversine formula
    a = (np.square(sin((phi2-phi1)/2)) + cos(phi1) * cos(phi2) *
         np.square(sin((lambda2-lambda1)/2)))
    d = 2*r*asin(np.sqrt(a))
    return d



my_lat = -27.46794
my_lon = 153.02809
#get_traffic_survey_near_user/<lat>/<lon>/<num_records>
#get_traffic_survey_near_user/-27.46794/153.02809/50
if 'distance' in list(df_traffic_census_2020.columns):
    df_traffic_census_2020.drop('distance', axis=1, inplace=True)

if 'distance2' in list(df_traffic_census_2020.columns):
    df_traffic_census_2020.drop('distance2', axis=1, inplace=True)

if 'distance' not in list(df_traffic_census_2020.columns):
    df_traffic_census_2020['distance']=-1

if 'distance2' not in list(df_traffic_census_2020.columns):
    df_traffic_census_2020['distance2']=-1

tic = time.perf_counter()
for ind in df_traffic_census_2020.index:
    lon2 = df_traffic_census_2020.loc[ind, 'LONGITUDE']
    lat2 = df_traffic_census_2020.loc[ind, 'LATITUDE']
    km = haversine_np(my_lon, my_lat, lon2, lat2)
    km2 = calculate_spherical_distance(my_lon, my_lat, lon2, lat2)
    df_traffic_census_2020.loc[ind,"distance"] = km
    df_traffic_census_2020.loc[ind,"distance2"] = km2

toc = time.perf_counter()
print(f"processed in {toc - tic:0.4f} seconds")
#processed in 0.2674 seconds
df_traffic_census_2020[['distance', 'distance2']]


tic = time.perf_counter()
df_traffic_census_2020.sort_values(['distance'], ascending=True, inplace=True)
toc = time.perf_counter()
print(f"processed in {toc - tic:0.4f} seconds")
#processed in 0.2891 seconds

df_traffic_census_2020.iloc[0:70]
#df_traffic_census_2020[df_traffic_census_2020['distance']<10]


df['distance'] = df.apply(lambda row: row.Cost -
                                  (row.Cost * 0.1), axis = 1)



from geopy.geocoders import Nominatim
import time
from pprint import pprint
app = Nominatim(user_agent="peerbanking.com.au")

#house wifi
latitude = -27.5633636
longitude = 153.0496858

#phone wifi
latitude = -27.5633621
longitude = 153.0496757
latitude = -27.563571
longitude = 153.0497328

coordinates = f"{latitude}, {longitude}"
coordinates
language="en"
results = app.reverse(coordinates, language=language).raw
results.keys()
# dict_keys(['place_id', 'licence', 'osm_type', 'osm_id', 'lat', 'lon', 'display_name', 'address', 'boundingbox'])
results['address'].keys()
# dict_keys(['house_number', 'road', 'city_district', 'city', 'state', 'ISO3166-2-lvl4', 'postcode', 'country', 'country_code'])


results['address']['house_number']
results['address']['road']
results['address']['city_district']
results['address']['city']
results['address']['state']
#
