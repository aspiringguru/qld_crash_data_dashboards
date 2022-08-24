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
df_crash_locations = pd.read_csv(input_fn_crash_locations)
print("startup : df_crash_locations.shape:", df_crash_locations.shape)
df_crash_locations.columns

list(df_crash_locations.columns)
"""
['Crash_Ref_Number', 'Crash_Severity', 'Crash_Year', 'Crash_Month',
'Crash_Day_Of_Week', 'Crash_Hour', 'Crash_Nature', 'Crash_Type', 'Crash_Longitude',
'Crash_Latitude', 'Crash_Street', 'Crash_Street_Intersecting', 'State_Road_Name',
'Loc_Suburb', 'Loc_Local_Government_Area', 'Loc_Post_Code',
'Loc_Police_Division', 'Loc_Police_District', 'Loc_Police_Region',
'Loc_Queensland_Transport_Region', 'Loc_Main_Roads_Region', 'Loc_ABS_Statistical_Area_2',
'Loc_ABS_Statistical_Area_3', 'Loc_ABS_Statistical_Area_4', 'Loc_ABS_Remoteness',
'Loc_State_Electorate', 'Loc_Federal_Electorate', 'Crash_Controlling_Authority',
'Crash_Roadway_Feature', 'Crash_Traffic_Control', 'Crash_Speed_Limit',
'Crash_Road_Surface_Condition', 'Crash_Atmospheric_Condition',
'Crash_Lighting_Condition', 'Crash_Road_Horiz_Align', 'Crash_Road_Vert_Align',
'Crash_DCA_Code', 'Crash_DCA_Description', 'Crash_DCA_Group_Description',
'DCA_Key_Approach_Dir', 'Count_Casualty_Fatality', 'Count_Casualty_Hospitalised',
'Count_Casualty_MedicallyTreated', 'Count_Casualty_MinorInjury', 'Count_Casualty_Total',
'Count_Unit_Car', 'Count_Unit_Motorcycle_Moped', 'Count_Unit_Truck', 'Count_Unit_Bus',
'Count_Unit_Bicycle', 'Count_Unit_Pedestrian', 'Count_Unit_Other']
"""


#'Crash_Street', 'State_Road_Name', 'Loc_Suburb', 'Loc_Local_Government_Area', 'Loc_Post_Code',

unique_addrs = list(df_crash_locations[['Crash_Street', 'State_Road_Name', 'Loc_Suburb', 'Loc_Local_Government_Area', 'Loc_Post_Code']].unique())

df_unique = pd.concat([df_crash_locations['Crash_Street'],df_crash_locations['State_Road_Name'],df_crash_locations['Loc_Suburb'],df_crash_locations['Loc_Local_Government_Area'],df_crash_locations['Loc_Post_Code']]).unique()
