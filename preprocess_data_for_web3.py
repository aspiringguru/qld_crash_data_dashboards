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

input_fn_alcohol_speed_fatigue = "crash_data_queensland_e_alcohol_speed_fatigue_defect.csv"
output_fn_alcohol_speed_fatigue = "crash_data_queensland_e_alcohol_speed_fatigue_defect.pkl"

df_alcohol_speed_fatigue=None
tic = time.perf_counter()
df_alcohol_speed_fatigue = pd.read_csv(input_fn_alcohol_speed_fatigue)
toc = time.perf_counter()
print(f"loaded from .csv file in {toc - tic:0.4f} seconds")
#loaded from .csv file in 0.2873 seconds

df_alcohol_speed_fatigue.to_pickle(output_fn_alcohol_speed_fatigue)
df_alcohol_speed_fatigue=None


tic = time.perf_counter()
df_alcohol_speed_fatigue = pd.read_pickle(output_fn_alcohol_speed_fatigue_defect)
toc = time.perf_counter()
print(f"loaded from pickle file in {toc - tic:0.4f} seconds")
#loaded from pickle file in 0.0232 seconds


print(f"csv loaded to dataframe in {toc - tic:0.4f} seconds")
print("startup : df_alcohol_speed_fatigue.shape:", df_alcohol_speed_fatigue.shape)
print("startup : df_alcohol_speed_fatigue.columns:", df_alcohol_speed_fatigue.columns)

'''
['Crash_Year', 'Crash_Police_Region', 'Crash_Severity',
       'Involving_Drink_Driving', 'Involving_Driver_Speed',
       'Involving_Fatigued_Driver', 'Involving_Defective_Vehicle',
       'Count_Crashes', 'Count_Fatality', 'Count_Hospitalised',
       'Count_Medically_Treated', 'Count_Minor_Injury',
       'Count_All_Casualties']
'''
list(df_alcohol_speed_fatigue['Crash_Year'].unique())
#[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
list(df_alcohol_speed_fatigue['Crash_Police_Region'].unique())
# ['Brisbane', 'Central', 'Far Northern', 'North Coast', 'Northern', 'South Eastern', 'Southern', 'Unknown']
list(df_alcohol_speed_fatigue['Crash_Severity'].unique())
# ['Fatal', 'Hospitalisation', 'Medical treatment', 'Minor injury', 'Property damage only']
list(df_alcohol_speed_fatigue['Involving_Drink_Driving'].unique())
# ['No', 'Yes']
list(df_alcohol_speed_fatigue['Involving_Driver_Speed'].unique())
# ['No', 'Yes']
list(df_alcohol_speed_fatigue['Involving_Fatigued_Driver'].unique())
# ['No', 'Yes']
list(df_alcohol_speed_fatigue['Involving_Defective_Vehicle'].unique())
# ['No', 'Yes']


#charts to make


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
df_years_post_codes_vehicle_type = pd.read_pickle(output_fn_crash_locations_vehicle_type_year_postcode_sums)
df_years_post_codes_vehicle_type.shape
df_years_post_codes_vehicle_type.columns
df_years_post_codes_vehicle_type
