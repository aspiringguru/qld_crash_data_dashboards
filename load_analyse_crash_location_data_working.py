"""
d:
cd D:\2020\coding\dashboard_demos
dashboard_env\Scripts\activate.bat
python


#geopandas can be installed with pip (difficult), conda = easier
https://geopandas.org/en/stable/docs/user_guide.html
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

list(df_crash_locations.columns)


['Crash_Ref_Number', 'Crash_Severity', 'Crash_Year', 'Crash_Month',
'Crash_Day_Of_Week', 'Crash_Hour', 'Crash_Nature', 'Crash_Type',
'Crash_Longitude', 'Crash_Latitude', 'Crash_Street', 'Crash_Street_Intersecting',
'State_Road_Name', 'Loc_Suburb', 'Loc_Local_Government_Area', 'Loc_Post_Code',
'Loc_Police_Division', 'Loc_Police_District', 'Loc_Police_Region',
'Loc_Queensland_Transport_Region', 'Loc_Main_Roads_Region',
'Loc_ABS_Statistical_Area_2', 'Loc_ABS_Statistical_Area_3',
'Loc_ABS_Statistical_Area_4', 'Loc_ABS_Remoteness', 'Loc_State_Electorate',
'Loc_Federal_Electorate', 'Crash_Controlling_Authority', 'Crash_Roadway_Feature',
'Crash_Traffic_Control', 'Crash_Speed_Limit', 'Crash_Road_Surface_Condition',
'Crash_Atmospheric_Condition', 'Crash_Lighting_Condition',
'Crash_Road_Horiz_Align', 'Crash_Road_Vert_Align', 'Crash_DCA_Code',
'Crash_DCA_Description', 'Crash_DCA_Group_Description', 'DCA_Key_Approach_Dir',
'Count_Casualty_Fatality', 'Count_Casualty_Hospitalised',
'Count_Casualty_MedicallyTreated', 'Count_Casualty_MinorInjury',
'Count_Casualty_Total', 'Count_Unit_Car', 'Count_Unit_Motorcycle_Moped',
'Count_Unit_Truck', 'Count_Unit_Bus', 'Count_Unit_Bicycle',
'Count_Unit_Pedestrian', 'Count_Unit_Other']

df_crash_locations.info()
df_crash_locations.describe()

categorical_colnames = ['Crash_Severity', 'Crash_Year', 'Crash_Month',
'Crash_Day_Of_Week', 'Crash_Hour', 'Crash_Nature', 'Crash_Type',
'Loc_Suburb', 'Loc_Local_Government_Area', 'Loc_Post_Code',
'Loc_Police_Division', 'Loc_Police_District', 'Loc_Police_Region',
'Loc_Queensland_Transport_Region', 'Loc_Main_Roads_Region',
'Loc_ABS_Statistical_Area_2', 'Loc_ABS_Statistical_Area_3',
'Loc_ABS_Statistical_Area_4', 'Loc_ABS_Remoteness', 'Loc_State_Electorate',
'Loc_Federal_Electorate', 'Crash_Controlling_Authority', 'Crash_Roadway_Feature',
'Crash_Traffic_Control', 'Crash_Speed_Limit', 'Crash_Road_Surface_Condition',
'Crash_Atmospheric_Condition', 'Crash_Lighting_Condition',
'Crash_Road_Horiz_Align', 'Crash_Road_Vert_Align', 'Crash_DCA_Code',
'Crash_DCA_Description', 'Crash_DCA_Group_Description', 'DCA_Key_Approach_Dir']
for categorical_colname in categorical_colnames:
    #print("categorical_colname:", categorical_colname)
    #df_crash_locations[categorical_colname].unique()
    print("{:40s} {:10s}".format(categorical_colname, str(len(list(df_crash_locations[categorical_colname].unique())))))
    print(categorical_colname+"\t\t\t:"+str(len(list(df_crash_locations[categorical_colname].unique()))))
    print("______________________________\n\n")

years       = list(df_crash_locations['Crash_Year'].unique())
Loc_Suburbs = list(df_crash_locations['Loc_Suburb'].unique())
Loc_Post_Codes = list(df_crash_locations['Loc_Post_Code'].unique())
len(Loc_Post_Codes) #454

>>> list(df_crash_locations['Crash_Nature'].unique())
['Head-on', 'Angle', 'Rear-end', 'Hit object', 'Overturned', 'Hit pedestrian', 'Sideswipe', 'Hit parked vehicle', 'Fall from vehicle', 'Non-collision - miscellaneous', 'Struck by external load', 'Collision - miscellaneous', 'Other', 'Hit animal', 'Struck by internal load']
>>> list(df_crash_locations['Crash_Type'].unique())
['Multi-Vehicle', 'Single Vehicle', 'Hit pedestrian', 'Other']
>>> list(df_crash_locations['Crash_Severity'].unique())
['Hospitalisation', 'Property damage only', 'Minor injury', 'Medical treatment', 'Fatal']

df_crash_locations.groupby(['Crash_Year'])['Loc_Suburb'].sum()
df_crash_locations_crash_yr_suburb_count = df_crash_locations.groupby(['Crash_Year', 'Loc_Post_Code'])['Crash_Year'].count()
df_crash_locations_crash_yr_suburb_count
df_crash_locations_crash_yr_suburb_sum.shape

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
df_years_post_codes_summary.to_pickle("crash_locations_years_post_codes_Crash_Severity_summary.csv")

df_years_post_codes_summary = pd.read_pickle("crash_locations_years_post_codes_Crash_Severity_summary.csv")
df_years_post_codes_summary.shape
df_years_post_codes_summary.columns


pd.concat(df_years_post_codes_summary, df_temp)

df_crash_locations[df_crash_locations['Crash_Year'] == year] #works

for year in years:
    print("year:", year)
    loc_Suburb_by_year = []
    for loc_Suburb in Loc_Suburbs:
        crash_count = df_crash_locations[(df_crash_locations['Crash_Year'] == year) & (df_crash_locations['Loc_Suburb'] == loc_Suburb)].shape[0]
        loc_Suburb_by_year.append(crash_count)
    print("loc_Suburb_by_year:", loc_Suburb_by_year)




#want to summarise this data to points with y crashes within x distance of point.
#mathematically and algo needed.
df_crash_locations[['Crash_Longitude', 'Crash_Latitude']].shape


Loc_Suburb
