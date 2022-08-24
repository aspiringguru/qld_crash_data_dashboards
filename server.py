"""
d:
cd D:\2020\coding\dashboard_demos
dashboard_env\Scripts\activate.bat
python server.py
"""

from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
import json
from config import *
import time
import numpy as np
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, acos, sqrt, pi

app = Flask(__name__)

input_data_fn = INPUT_DATA_FN
df = pd.read_csv(input_data_fn)
print("startup : df.shape:", df.shape)

"""
#avoid loading the full crash dataset, too large and slow to load.
input_fn_crash_locations = "crash_data_queensland_1_crash_locations.csv"
df_crash_locations = pd.read_csv(input_fn_crash_locations)
print("startup : df_crash_locations.shape:", df_crash_locations.shape)
"""
output_fn_crash_locations_crash_severity = OUTPUT_FN_CRASH_LOCATIONS_CRASH_SEVERITY
print("loading crash locations data. output_fn_crash_locations_crash_severity:", output_fn_crash_locations_crash_severity)
df_years_post_codes_summary = pd.read_pickle(output_fn_crash_locations_crash_severity)
print("crash locations data loaded.")
print("df_years_post_codes_summary.shape:", df_years_post_codes_summary.shape)
print("df_years_post_codes_summary.columns:", df_years_post_codes_summary.columns)

output_fn_crash_locations_vehicle_type_year_postcode_sums = OUTPUT_FN_CRASH_LOCATIONS_VEHICLE_TYPE_YEAR_POSTCODE
df_years_post_codes_vehicle_type = pd.read_pickle(output_fn_crash_locations_vehicle_type_year_postcode_sums)
print("df_years_post_codes_vehicle_type.shape:", df_years_post_codes_vehicle_type.shape)
print("df_years_post_codes_vehicle_type.columns:", df_years_post_codes_vehicle_type.columns)

output_fn_alcohol_speed_fatigue_defect = OUTPUT_FN_ALCOHOL_SPEED_FATIGUE_DEFECT
df_alcohol_speed_fatigue_defect = pd.read_pickle(output_fn_alcohol_speed_fatigue_defect)
print("df_alcohol_speed_fatigue_defect.shape:",   df_alcohol_speed_fatigue_defect.shape)
print("df_alcohol_speed_fatigue_defect.columns:", df_alcohol_speed_fatigue_defect.columns)

input_fn_traffic_census_2020 = INPUT_FN_TRAFFIC_CENSUS_2020
df_traffic_census_2020 = pd.read_csv(input_fn_traffic_census_2020)
print("df_traffic_census_2020.shape:", df_traffic_census_2020.shape)
print("df_traffic_census_2020.columns:", df_traffic_census_2020.columns)


#@app.route('/get_crash_locations_postcode_by_year/<year>')
#def get_crash_locations_postcode_by_year(year):
#    print("route:get_crash_locations_postcode_by_year:year:", year)

@app.route('/get_users_address/<my_lat>/<my_lon>')
def get_users_address(my_lat, my_lon):
    print("@app.route:/get_users_address:my_lat:", my_lat)
    print("@app.route:/get_users_address:my_lon:", my_lon)
    app = Nominatim(user_agent="peerbanking.com.au")
    coordinates = f"{my_lat}, {my_lon}"
    language="en"
    try:
        time.sleep(1) #good usage policy. avoid overuse.
        results = app.reverse(coordinates, language=language).raw
        #results['address']['house_number']
        #results['address']['road']
        #results['address']['city_district']
        #results['address']['city']
        #results['address']['state']
        return results
    except:
        return { "error":"error"}

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    All args must be of equal length.
    """
    #print("haversine_np:type(lon1)", type(lon1))
    #print("haversine_np:type(lat1)", type(lat1))
    #print("haversine_np:type(lon2)", type(lon2))
    #print("haversine_np:type(lat2)", type(lat2))
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


@app.route('/get_traffic_survey_near_user/<my_lat>/<my_lon>/<num_records>')
def get_traffic_survey_near_user(my_lat, my_lon, num_records):
    #print("@app.route:/get_traffic_survey_near_user:my_lat:", my_lat)
    #print("@app.route:/get_traffic_survey_near_user:my_lon:", my_lon)
    #print("@app.route:/get_traffic_survey_near_user:type(my_lat):", type(my_lat))
    #print("@app.route:/get_traffic_survey_near_user:type(my_lon):", type(my_lon))
    #print("@app.route:/get_traffic_survey_near_user:num_records:", num_records)
    #print("@app.route:/get_traffic_survey_near_user:df_traffic_census_2020.shape:", df_traffic_census_2020.shape)
    my_lon = float(my_lon)
    my_lat = float(my_lat)
    num_records = int(num_records)
    #
    if 'distance' in list(df_traffic_census_2020.columns):
        df_traffic_census_2020.drop('distance', axis=1, inplace=True)
    if 'distance' not in list(df_traffic_census_2020.columns):
        df_traffic_census_2020['distance']=-1
    """
    if 'distance2' in list(df_traffic_census_2020.columns):
        df_traffic_census_2020.drop('distance2', axis=1, inplace=True)
    if 'distance2' not in list(df_traffic_census_2020.columns):
        df_traffic_census_2020['distance2']=-1
    """
    tic = time.perf_counter()
    for ind in df_traffic_census_2020.index:
        lon2 = df_traffic_census_2020.loc[ind, 'LONGITUDE']
        lat2 = df_traffic_census_2020.loc[ind, 'LATITUDE']
        km = haversine_np(my_lon, my_lat, lon2, lat2)
        df_traffic_census_2020.loc[ind,"distance"] = km
        #km2 = calculate_spherical_distance(my_lon, my_lat, lon2, lat2)
        #df_traffic_census_2020.loc[ind,"distance2"] = km2
    #
    toc = time.perf_counter()
    print(f"distance columne added : processed in {toc - tic:0.4f} seconds")
    #processed in 0.2674 seconds
    tic = time.perf_counter()
    df_traffic_census_2020.sort_values(['distance'], ascending=True, inplace=True)
    toc = time.perf_counter()
    print(f"sorted by distance columns : processed in {toc - tic:0.4f} seconds")
    return json.loads(df_traffic_census_2020.iloc[0:num_records].to_json(orient="table"))


@app.route('/get_traffic_survey_2020')
def get_traffic_survey_2020():
    print("@app.route:/get_traffic_survey_2020:df_traffic_census_2020.shape:", df_traffic_census_2020.shape)
    return json.loads(df_traffic_census_2020.to_json(orient="table"))


@app.route('/get_alcohol_speed_fatigue_defect')
def get_alcohol_speed_fatigue_defect():
    print("@app.route:/get_alcohol_speed_fatigue_defect:df_alcohol_speed_fatigue_defect.shape:", df_alcohol_speed_fatigue_defect.shape)
    return json.loads(df_alcohol_speed_fatigue_defect.to_json(orient="table"))

@app.route('/get_alcohol_speed_fatigue_defect_years')
def get_alcohol_speed_fatigue_defect_years():
    print("@app.route:/get_alcohol_speed_fatigue_defect_years:df_alcohol_speed_fatigue_defect.shape:", df_alcohol_speed_fatigue_defect.shape)
    years = df_alcohol_speed_fatigue_defect['Crash_Year'].unique().tolist()
    print("years:", years)
    print("type(years[0]):", type(years[0]))
    return jsonify({"years": years})


@app.route('/get_crash_locations_years')
def get_crash_locations_years():
    print("@app.route:/get_crash_locations_years:df_years_post_codes_summary.shape:", df_years_post_codes_summary.shape)
    years = list(df_years_post_codes_summary['year'].unique())
    print("years:", years)
    print("type(years[0]):", type(years[0]))
    return jsonify({"years": years})

@app.route('/get_crash_locations_postcode')
def get_crash_locations_postcode():
    print("@app.route:/get_crash_locations_postcode:df.shape:", df_years_post_codes_summary.shape)
    return json.loads(df_years_post_codes_summary.to_json(orient="table"))

@app.route('/get_crash_locations_postcode_by_year/<year>')
def get_crash_locations_postcode_by_year(year):
    print("route:get_crash_locations_postcode_by_year:year:", year)
    print("type(year):", type(year))
    year = int(year)
    print("df_years_post_codes_summary.shape:", df_years_post_codes_summary.shape)
    df_year = df_years_post_codes_summary[df_years_post_codes_summary['year'] == year]
    print("df_year.shape:", df_year.shape)
    return json.loads(df_year.to_json(orient="table"))

@app.route('/get_crash_vehicle_type_by_year_by_postcode/<year>')
def get_crash_vehicle_type_by_year(year):
    print("route:get_crash_vehicle_type_by_year_by_postcode:year", year)
    print("type(year):", type(year))
    year = int(year)
    print("df_years_post_codes_vehicle_type.shape:", df_years_post_codes_vehicle_type.shape)
    df_year = df_years_post_codes_vehicle_type[df_years_post_codes_vehicle_type['year'] == year]
    print("df_year:", df_year)
    return json.loads(df_year.to_json(orient="table"))

@app.route('/get_crash_locations_vehicle_types_years')
def get_crash_locations_vehicle_types_years():
    print("@app.route:/get_crash_locations_vehicle_types_years:df_years_post_codes_vehicle_type.shape:", df_years_post_codes_vehicle_type.shape)
    years = list(df_years_post_codes_vehicle_type['year'].unique())
    return jsonify({"years": years})



@app.route('/get_data')
def get_data():
    print("@app.route:/get_data2:df.shape:", df.shape)
    return json.loads(df.to_json(orient="table"))
    #return "this is @app.route:/get_data2"

@app.route('/get_Crash_Police_Regions')
def get_Crash_Police_Regions():
    print("@app.route:/get_Crash_Police_Regions:df.shape:", df.shape)
    temp_dict = {"Crash_Police_Region": list(df['Crash_Police_Region'].unique())}
    return json.loads(json.dumps(temp_dict))

@app.route('/get_Count_Crashes_By_Year')
def get_Count_Crashes_By_Year():
    temp_df = df.groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
    print("temp_df:", temp_df)
    result = temp_df.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed

@app.route('/get_Count_Crashes_By_Year_Region')
def get_Count_Crashes_By_Year_Region():
    years_ = list(df['Crash_Year'].unique())
    df_regions  = pd.DataFrame()
    df_regions['Crash_Year'] = years_
    regions = list(df['Crash_Police_Region'].unique())
    for region in regions:
        df_region = df[df['Crash_Police_Region'] == region].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
        df_region.rename(columns = {'Count_Crashes':region}, inplace = True)
        df_temp = df_regions.merge(df_region, how='left')
        df_regions = df_temp
    #
    df_regions.fillna(value=0, inplace=True)
    result = df_regions.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed

@app.route('/get_Count_Crashes_By_Year_By_Gender')
def get_Count_Crashes_By_Year_By_Gender():
    temp_df = df.groupby(['Crash_Year', 'Involving_Male_Driver', 'Involving_Female_Driver'])['Count_Crashes'].sum().reset_index()
    print("temp_df:", temp_df)
    result = temp_df.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed


@app.route('/get_Count_Crashes_By_Year_By_Age')
def get_Count_Crashes_By_Year_By_Age():
    temp_df = df.groupby(['Crash_Year', 'Involving_Young_Driver_16-24', 'Involving_Senior_Driver_60plus'])['Count_Crashes'].sum().reset_index()
    print("temp_df:", temp_df)
    result = temp_df.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed


@app.route('/get_Count_Crashes_By_Year_By_Provisional_Driver')
def get_Count_Crashes_By_Year_By_Provisional_Driver():
    temp_df = df.groupby(['Crash_Year', 'Involving_Provisional_Driver'])['Count_Crashes'].sum().reset_index()
    print("temp_df:", temp_df)
    result = temp_df.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed


@app.route('/get_Count_Crashes_By_Year_By_Overseas_Licensed_Driver')
def get_Count_Crashes_By_Year_By_Overseas_Licensed_Driver():
    df_OS_yes = df[df['Involving_Overseas_Licensed_Driver'] == "Yes"].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
    df_OS_yes.rename(columns = {'Count_Crashes':'Overseas_Licensed_Driver'}, inplace = True)
    #
    df_OS_no  = df[df['Involving_Overseas_Licensed_Driver'] == "No"].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
    df_OS_no.rename(columns = {'Count_Crashes':'Australian_Licenced_Driver'}, inplace = True)
    #merge df_OS_no & df_OS_yes,
    df_merged = df_OS_yes.merge(df_OS_no, how='outer').fillna(0)
    print("df_merged:", df_merged)
    result = df_merged.to_json(orient="split")
    #print("result:", result)
    parsed = json.loads(result)
    return parsed



@app.route('/get_colnames')
def get_colnames():
    print("@app.route:/get_colnames")
    temp_dict = {"columns": list(df.columns)}
    return json.loads(json.dumps(temp_dict))

@app.route('/get_col_unique_2_json/<col_name>')
def get_col_unique_2_json(col_name):
    print("@app.route:/get_col_unique_2_json:col_name:", col_name)
    if is_string_dtype(df[col_name]):
        temp_dict = {col_name: list(df[col_name].unique())}
        return json.loads(json.dumps(temp_dict))
    else:
        return {"error":"not string column"}

@app.route('/get_max_min/<col_name>')
def get_max_min(col_name):
    print("@app.route:/get_max_min:col_name:", col_name)
    if is_numeric_dtype(df[col_name]):
        temp_dict = {col_name:{"max": str(df[col_name].max()), "min":str(df[col_name].min())}}
        return json.loads(json.dumps(temp_dict))
    else:
        return {"error":"not numeric column"}

@app.route("/get_html/<filename>")
def get_html(filename):
    #print("route get_html:", filename)
    return render_template(filename)

@app.route('/get_routes')
def get_routes():
    print("get_routes")
    map_ = app.url_map
    print("app.url_map:", map_)
    print("type(map_):", type(map_))
    return str(map_)


@app.route('/')
def home():
    print("@app.route:/")
    return render_template("index.html")


if __name__ == '__main__':
    print("start flask server main method.")
    app.run(host='0.0.0.0', debug = DEBUG, port=PORT)
