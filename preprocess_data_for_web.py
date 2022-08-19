"""
d:
cd D:\2020\coding\dashboard_demos
dashboard_env\Scripts\activate.bat
python
"""
import time
import pandas as pd
import time
import sqlite3
from sqlite3 import Error
import json
from json import JSONEncoder
import numpy

input_fn_crash_locations = "crash_data_queensland_1_crash_locations.csv"
output_fn_crash_locations_crash_severity = "crash_locations_years_post_codes_Crash_Severity_summary.pkl"
output_fn_crash_locations_vehicle_type_year_postcode_sums = "crash_locations_vehicle_type_year_postcode_sums.pkl"


df_crash_locations = pd.read_csv(input_fn_crash_locations)
print("startup : df_crash_locations.shape:", df_crash_locations.shape)


tic = time.perf_counter()
years       = list(df_crash_locations['Crash_Year'].unique())
Loc_Post_Codes = list(df_crash_locations['Loc_Post_Code'].unique())
colnames_ = ['year', 'post_code', 'count_all', 'count_hospitalisation', 'count_property', 'count_minor', 'count_medical', 'count_fatal']
df_years_post_codes_summary = pd.DataFrame(columns = colnames_)


for year in years:
    print("year:", year)
    for Loc_Post_Code in Loc_Post_Codes:
        print("Loc_Post_Code:", Loc_Post_Code)
        count_All = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code)].shape[0]
        count_Hospitalisation = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code) & (df_crash_locations['Crash_Severity']=='Hospitalisation')].shape[0]
        count_Prop = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code) & (df_crash_locations['Crash_Severity']=='Property damage only')].shape[0]
        count_Minor = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code) & (df_crash_locations['Crash_Severity']=='Minor injury')].shape[0]
        count_Medical = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code) & (df_crash_locations['Crash_Severity']=='Medical treatment')].shape[0]
        count_Fatal = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code) & (df_crash_locations['Crash_Severity']=='Fatal')].shape[0]
        list_ = [year, Loc_Post_Code, count_All, count_Hospitalisation, count_Prop, count_Minor, count_Medical, count_Fatal]
        df_temp = pd.DataFrame( [list_], columns=colnames_)
        print("df_temp:", df_temp)
        df_years_post_codes_summary = pd.concat([df_years_post_codes_summary, df_temp])

print("df_years_post_codes_summary:\n", df_years_post_codes_summary)
toc = time.perf_counter()
print(f"completed in {toc - tic:0.4f} seconds")
df_years_post_codes_summary.to_pickle(output_fn_crash_locations_crash_severity)

df_years_post_codes_summary = pd.read_pickle(output_fn_crash_locations_crash_severity)
df_years_post_codes_summary.shape
df_years_post_codes_summary.columns

#-------------------------------------------------------------------------------

tic = time.perf_counter()
years       = list(df_crash_locations['Crash_Year'].unique())
Loc_Post_Codes = list(df_crash_locations['Loc_Post_Code'].unique())
colnames_ = ['year', 'post_code', 'count_events', 'Count_Unit_Car', 'Count_Unit_Motorcycle_Moped', 'Count_Unit_Truck', 'Count_Unit_Bus', 'Count_Unit_Bicycle', 'Count_Unit_Pedestrian', 'Count_Unit_Other']
df_years_post_codes_vehicle_type = pd.DataFrame(columns = colnames_)

for year in years:
    print("year:", year)
    for Loc_Post_Code in Loc_Post_Codes:
        print("Loc_Post_Code:", Loc_Post_Code)
        df_year_pcode = df_crash_locations[(df_crash_locations['Crash_Year']==year) & (df_crash_locations['Loc_Post_Code']==Loc_Post_Code)]
        df_year_pcode_num_events = df_year_pcode.shape[0]
        #df_year_pcode_num_events
        df_year_pcode_summary_ = df_year_pcode[['Count_Unit_Car', 'Count_Unit_Motorcycle_Moped', 'Count_Unit_Truck', 'Count_Unit_Bus', 'Count_Unit_Bicycle', 'Count_Unit_Pedestrian', 'Count_Unit_Other']]
        df_row = df_year_pcode_summary_.sum(axis=0).to_frame().T
        df_row['year'] = year
        df_row['post_code'] = Loc_Post_Code
        df_row['count_events'] = df_year_pcode_num_events
        df_row
        df_years_post_codes_vehicle_type = pd.concat([df_years_post_codes_vehicle_type, df_row])

#print("df_years_post_codes_vehicle_type:\n", df_years_post_codes_vehicle_type)
toc = time.perf_counter()
print(f"completed in {toc - tic:0.4f} seconds")
df_years_post_codes_vehicle_type.to_pickle(output_fn_crash_locations_vehicle_type_year_postcode_sums)
df_years_post_codes_vehicle_type=None
df_years_post_codes_vehicle_type = pd.read_pickle(output_fn_crash_locations_crash_severity)
df_years_post_codes_vehicle_type.shape
df_years_post_codes_vehicle_type.columns
