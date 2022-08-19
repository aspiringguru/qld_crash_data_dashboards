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

app = Flask(__name__)

input_data_fn = "crash_data_queensland_b_driver_involvement.csv"
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
