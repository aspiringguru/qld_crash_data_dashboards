"""
d:
cd D:\2020\coding\dashboard_demos
dashboard_env\Scripts\activate.bat
python


d:
cd D:\2020\coding\dashboard_demos
python -m venv dashboard_env
dashboard_env\Scripts\activate.bat
pip install pandas

"""

import pandas as pd
import time
import sqlite3
from sqlite3 import Error
import json
from json import JSONEncoder
import numpy

db_filename="road_crash_data.db"
conn = sqlite3.connect(db_filename)

input_data_fn = "crash_data_queensland_b_driver_involvement.csv"
df = pd.read_csv(input_data_fn)
df.shape
df.columns
df.info()
df.describe()


from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
for colname in df.columns:
    "colname:", colname
    df[colname].describe()
    "dtypes:", df[colname].dtypes
    "is_numeric_dtype:", is_numeric_dtype(df[colname])
    "is_string_dtype:", is_string_dtype(df[colname])
    ""

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


df['Crash_Police_Region'].unique()
type(df['Crash_Police_Region'].unique())
numpyData = {"Crash_Police_Region": df['Crash_Police_Region'].unique()}
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
encodedNumpyData

temp_dict = {"Crash_Police_Region": list(df['Crash_Police_Region'].unique())}
temp_dict
json.dumps(temp_dict)

#get crash count by year.
#'Crash_Year', 'Count_Crashes'

df.groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()

df.groupby(['Crash_Year', 'Involving_Male_Driver'])['Count_Crashes'].sum().reset_index()
df.groupby(['Crash_Year', 'Involving_Male_Driver', 'Involving_Female_Driver'])['Count_Crashes'].sum().reset_index()

'Involving_Male_Driver', 'Involving_Female_Driver'


df[['Crash_Year','Involving_Provisional_Driver', 'Involving_Overseas_Licensed_Driver', 'Involving_Unlicensed_Driver', 'Count_Crashes']].loc[df['Crash_Year'] == 2020].shape

df.loc[df['Crash_Year'] == 2020].shape


df.groupby(['Crash_Year', 'Involving_Overseas_Licensed_Driver'])['Count_Crashes'].sum().reset_index()

df[df['Involving_Overseas_Licensed_Driver'] == "Yes"].shape
df_OS_yes = df[df['Involving_Overseas_Licensed_Driver'] == "Yes"].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
df_OS_yes.rename(columns = {'Count_Crashes':'Overseas_Licensed_Driver'}, inplace = True)
#
df_OS_no  = df[df['Involving_Overseas_Licensed_Driver'] == "No"].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
df_OS_no.rename(columns = {'Count_Crashes':'Australian_Licenced_Driver'}, inplace = True)
#merge df_OS_no & df_OS_yes,
df_OS_yes.merge(df_OS_no, how='outer').fillna(0)


df[df['Involving_Overseas_Licensed_Driver'] == "Yes"].shape

list(df.columns)
list(df['Crash_Police_Region'].unique())
array(['Brisbane', 'Central', 'Far Northern', 'North Coast', 'Northern',
       'South Eastern', 'Southern', 'Unknown'], dtype=object)

df[df['Crash_Police_Region'] == "Brisbane"].shape
df[df['Crash_Police_Region'] == "Brisbane"].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()

years_ = list(df['Crash_Year'].unique())
years_
#create dataframe with column 'Crash_Year' set to these values, then merge dataframes onto this df.
df_regions  = pd.DataFrame()
df_regions['Crash_Year'] = years_
df_regions


regions = list(df['Crash_Police_Region'].unique())
for region in regions:
    df_region = df[df['Crash_Police_Region'] == region].groupby(['Crash_Year'])['Count_Crashes'].sum().reset_index()
    df_region.rename(columns = {'Count_Crashes':region}, inplace = True)
    df_temp = df_regions.merge(df_region, how='left')
    df_regions = df_temp

df_regions.fillna(value=0, inplace=True)


#-------------------------------------------------------------------------------
#https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads
Road crash locations APICSV
Location and characteristics of crashes within Queensland for all reported...

Road casualties APICSV
Characteristics of casualties as a result of crashes within Queensland for...

Driver demographics APICSV
Driver involvement in crashes within Queensland for all reported Road Traffic...

Seatbelt restraints and helmet use APICSV
Restraint use of vehicle occupant casualties, and helmet use of motorcycle...

Vehicle types APICSV
Vehicle involvement in crashes within Queensland for all reported Road...

Factors in road crashes APICSV
Alcohol, speed, fatigue and defective vehicle involvement in crashes within...
#-------------------------------------------------------------------------------


crash_location_fn = "crash_data_queensland_1_crash_locations.csv"
crash_loc_df = pd.read_csv(crash_location_fn)
crash_loc_df.columns
crash_loc_df.shape
#(360528, 52)
#['Crash_Ref_Number', 'Crash_Severity', 'Crash_Year', 'Crash_Month',
       'Crash_Day_Of_Week', 'Crash_Hour', 'Crash_Nature', 'Crash_Type',
       'Crash_Longitude', 'Crash_Latitude', 'Crash_Street',
       'Crash_Street_Intersecting', 'State_Road_Name', 'Loc_Suburb',
       'Loc_Local_Government_Area', 'Loc_Post_Code', 'Loc_Police_Division',
       'Loc_Police_District', 'Loc_Police_Region',
       'Loc_Queensland_Transport_Region', 'Loc_Main_Roads_Region',
       'Loc_ABS_Statistical_Area_2', 'Loc_ABS_Statistical_Area_3',
       'Loc_ABS_Statistical_Area_4', 'Loc_ABS_Remoteness',
       'Loc_State_Electorate', 'Loc_Federal_Electorate',
       'Crash_Controlling_Authority', 'Crash_Roadway_Feature',
       'Crash_Traffic_Control', 'Crash_Speed_Limit',
       'Crash_Road_Surface_Condition', 'Crash_Atmospheric_Condition',
       'Crash_Lighting_Condition', 'Crash_Road_Horiz_Align',
       'Crash_Road_Vert_Align', 'Crash_DCA_Code', 'Crash_DCA_Description',
       'Crash_DCA_Group_Description', 'DCA_Key_Approach_Dir',
       'Count_Casualty_Fatality', 'Count_Casualty_Hospitalised',
       'Count_Casualty_MedicallyTreated', 'Count_Casualty_MinorInjury',
       'Count_Casualty_Total', 'Count_Unit_Car', 'Count_Unit_Motorcycle_Moped',
       'Count_Unit_Truck', 'Count_Unit_Bus', 'Count_Unit_Bicycle',
       'Count_Unit_Pedestrian', 'Count_Unit_Other']



#https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads/resource/177dc50c-0cf7-46ba-8a69-99695aeaa46a
crash_restraints_fn = "crash_data_queensland_c_restraint_helmet_use.csv"
crash_restraints_df = pd.read_csv(crash_restraints_fn)
crash_restraints_df.shape
crash_restraints_df.columns

(35765, 8)
['Crash_Year', 'Crash_PoliceRegion', 'Casualty_Severity',
       'Casualty_AgeGroup', 'Casualty_Gender', 'Casualty_Road_User_Type',
       'Casualty_Restraint_Helmet_Use', 'Casualty_Count'],
      dtype='object')


#https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads/resource/f999155b-37f7-48aa-b5dd-644838130b0b
crash_vehicle_type_fn = "crash_data_queensland_d_vehicle_involvement.csv"
crash_vehicle_type_df = pd.read_csv(crash_vehicle_type_fn)
crash_vehicle_type_df.shape
crash_vehicle_type_df.columns
#
(3229, 12)
>>> crash_vehicle_type_df.columns
['Crash_Year', 'Crash_Police_Region', 'Crash_Severity',
'Involving_Motorcycle_Moped', 'Involving_Truck', 'Involving_Bus',
'Count_Crashes', 'Count_Casualty_Fatality',
'Count_Casualty_Hospitalised', 'Count_Casualty_MedicallyTreated',
'Count_Casualty_MinorInjury', 'Count_Casualty_All'],


#https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads/resource/18ee2911-992f-40ed-b6ae-e756859786e6
crash_vehicle_type_fn = "crash_data_queensland_e_alcohol_speed_fatigue_defect.csv"
crash_vehicle_type_df = pd.read_csv(crash_vehicle_type_fn)
crash_vehicle_type_df.shape
crash_vehicle_type_df.columns

(4777, 13)
['Crash_Year', 'Crash_Police_Region', 'Crash_Severity',
'Involving_Drink_Driving', 'Involving_Driver_Speed',
'Involving_Fatigued_Driver', 'Involving_Defective_Vehicle',
'Count_Crashes', 'Count_Fatality', 'Count_Hospitalised',
'Count_Medically_Treated', 'Count_Minor_Injury',
'Count_All_Casualties'],


https://www.data.qld.gov.au/dataset/active-mobile-speed-camera-sites



list(df_crash_locations['Crash_Speed_Limit'].unique())
['0 - 50 km/h', '60 km/h', '70 km/h', '80 - 90 km/h', '100 - 110 km/h', nan]


'Count_Unit_Car', 'Count_Unit_Motorcycle_Moped', 'Count_Unit_Truck', 'Count_Unit_Bus', 'Count_Unit_Bicycle', 'Count_Unit_Pedestrian', 'Count_Unit_Other'

output_fn_crash_locations_vehicle_type_year_postcode_sums = "crash_locations_vehicle_type_year_postcode_sums.pkl"
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
