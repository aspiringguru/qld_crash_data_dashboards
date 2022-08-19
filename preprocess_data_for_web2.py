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


input_fn_crash_vehicle_type = "crash_data_queensland_d_vehicle_involvement.csv"
output_fn_crash_locations_vehicle_type_year_postcode_sums = "crash_locations_vehicle_type_year_postcode_sums.pkl"

df_crash_vehicle_type = pd.read_csv(input_fn_crash_vehicle_type)
print("startup : df_crash_vehicle_type.shape:", df_crash_vehicle_type.shape)


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
        df_year_pcode = df_crash_vehicle_type[(df_crash_vehicle_type['Crash_Year']==year) & (df_crash_vehicle_type['Loc_Post_Code']==Loc_Post_Code)]
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
df_years_post_codes_vehicle_type = pd.read_pickle(output_fn_crash_locations_vehicle_type_year_postcode_sums)
df_years_post_codes_vehicle_type.shape
df_years_post_codes_vehicle_type.columns
df_years_post_codes_vehicle_type
