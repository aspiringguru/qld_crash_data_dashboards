/*
d:
cd D:\2020\coding\dashboard_demos
sqlite3 crash_data_queensland.db

cd /mnt/d/2020/coding/dashboard_demos


crash_data_queensland_1_crash_locations.csv
crash_data_queensland_c_restraint_helmet_use.csv
crash_data_queensland_e_alcohol_speed_fatigue_defect.csv
crash_data_queensland_b_driver_involvement.csv
crash_data_queensland_d_vehicle_involvement.csv
*/

.mode csv
.import crash_data_queensland_1_crash_locations.csv crash_locations
.import crash_data_queensland_c_restraint_helmet_use.csv restraint_helmet_use
.import crash_data_queensland_e_alcohol_speed_fatigue_defect.csv alcohol_speed_fatigue_defect
.import crash_data_queensland_b_driver_involvement.csv driver_involvement
.import crash_data_queensland_d_vehicle_involvement.csv vehicle_involvement

.import data/trafficcensus2020.csv trafficcensus2020


#-----------------------------------------------
.schema
CREATE TABLE IF NOT EXISTS "crash_locations"(
  "Crash_Ref_Number" TEXT,
  "Crash_Severity" TEXT,
  "Crash_Year" TEXT,
  "Crash_Month" TEXT,
  "Crash_Day_Of_Week" TEXT,
  "Crash_Hour" TEXT,
  "Crash_Nature" TEXT,
  "Crash_Type" TEXT,
  "Crash_Longitude" TEXT,
  "Crash_Latitude" TEXT,
  "Crash_Street" TEXT,
  "Crash_Street_Intersecting" TEXT,
  "State_Road_Name" TEXT,
  "Loc_Suburb" TEXT,
  "Loc_Local_Government_Area" TEXT,
  "Loc_Post_Code" TEXT,
  "Loc_Police_Division" TEXT,
  "Loc_Police_District" TEXT,
  "Loc_Police_Region" TEXT,
  "Loc_Queensland_Transport_Region" TEXT,
  "Loc_Main_Roads_Region" TEXT,
  "Loc_ABS_Statistical_Area_2" TEXT,
  "Loc_ABS_Statistical_Area_3" TEXT,
  "Loc_ABS_Statistical_Area_4" TEXT,
  "Loc_ABS_Remoteness" TEXT,
  "Loc_State_Electorate" TEXT,
  "Loc_Federal_Electorate" TEXT,
  "Crash_Controlling_Authority" TEXT,
  "Crash_Roadway_Feature" TEXT,
  "Crash_Traffic_Control" TEXT,
  "Crash_Speed_Limit" TEXT,
  "Crash_Road_Surface_Condition" TEXT,
  "Crash_Atmospheric_Condition" TEXT,
  "Crash_Lighting_Condition" TEXT,
  "Crash_Road_Horiz_Align" TEXT,
  "Crash_Road_Vert_Align" TEXT,
  "Crash_DCA_Code" TEXT,
  "Crash_DCA_Description" TEXT,
  "Crash_DCA_Group_Description" TEXT,
  "DCA_Key_Approach_Dir" TEXT,
  "Count_Casualty_Fatality" TEXT,
  "Count_Casualty_Hospitalised" TEXT,
  "Count_Casualty_MedicallyTreated" TEXT,
  "Count_Casualty_MinorInjury" TEXT,
  "Count_Casualty_Total" TEXT,
  "Count_Unit_Car" TEXT,
  "Count_Unit_Motorcycle_Moped" TEXT,
  "Count_Unit_Truck" TEXT,
  "Count_Unit_Bus" TEXT,
  "Count_Unit_Bicycle" TEXT,
  "Count_Unit_Pedestrian" TEXT,
  "Count_Unit_Other" TEXT
);
CREATE TABLE IF NOT EXISTS "restraint_helmet_use"(
  "Crash_Year" TEXT,
  "Crash_PoliceRegion" TEXT,
  "Casualty_Severity" TEXT,
  "Casualty_AgeGroup" TEXT,
  "Casualty_Gender" TEXT,
  "Casualty_Road_User_Type" TEXT,
  "Casualty_Restraint_Helmet_Use" TEXT,
  "Casualty_Count" TEXT
);
CREATE TABLE IF NOT EXISTS "alcohol_speed_fatigue_defect"(
  "Crash_Year" TEXT,
  "Crash_Police_Region" TEXT,
  "Crash_Severity" TEXT,
  "Involving_Drink_Driving" TEXT,
  "Involving_Driver_Speed" TEXT,
  "Involving_Fatigued_Driver" TEXT,
  "Involving_Defective_Vehicle" TEXT,
  "Count_Crashes" TEXT,
  "Count_Fatality" TEXT,
  "Count_Hospitalised" TEXT,
  "Count_Medically_Treated" TEXT,
  "Count_Minor_Injury" TEXT,
  "Count_All_Casualties" TEXT
);
CREATE TABLE IF NOT EXISTS "driver_involvement"(
  "Crash_Year" TEXT,
  "Crash_Police_Region" TEXT,
  "Crash_Severity" TEXT,
  "Involving_Male_Driver" TEXT,
  "Involving_Female_Driver" TEXT,
  "Involving_Young_Driver_16-24" TEXT,
  "Involving_Senior_Driver_60plus" TEXT,
  "Involving_Provisional_Driver" TEXT,
  "Involving_Overseas_Licensed_Driver" TEXT,
  "Involving_Unlicensed_Driver" TEXT,
  "Count_Crashes" TEXT,
  "Count_Casualty_Fatality" TEXT,
  "Count_Casualty_Hospitalised" TEXT,
  "Count_Casualty_MedicallyTreated" TEXT,
  "Count_Casualty_MinorInjury" TEXT,
  "Count_Casualty_All" TEXT
);
CREATE TABLE IF NOT EXISTS "vehicle_involvement"(
  "Crash_Year" TEXT,
  "Crash_Police_Region" TEXT,
  "Crash_Severity" TEXT,
  "Involving_Motorcycle_Moped" TEXT,
  "Involving_Truck" TEXT,
  "Involving_Bus" TEXT,
  "Count_Crashes" TEXT,
  "Count_Casualty_Fatality" TEXT,
  "Count_Casualty_Hospitalised" TEXT,
  "Count_Casualty_MedicallyTreated" TEXT,
  "Count_Casualty_MinorInjury" TEXT,
  "Count_Casualty_All" TEXT
);
#-----------------------------------------------

.tables
drop table crash_locations;
drop table alcohol_speed_fatigue_defect;
drop table restraint_helmet_use;
drop table driver_involvement;
drop table vehicle_involvement;


.schema crash_locations


select distinct Crash_Road_Surface_Condition from crash_locations;
"Sealed - Dry"
"Unsealed - Dry"
"Sealed - Wet"
Unknown
"Unsealed - Wet"

select distinct Crash_Atmospheric_Condition from crash_locations;
Clear
Raining
Unknown
Fog
Smoke/Dust

select distinct Crash_Lighting_Condition from crash_locations;
Daylight
"Darkness - Lighted"
Dawn/Dusk
"Darkness - Not lighted"
Unknown

select distinct Crash_Road_Horiz_Align from crash_locations;
"Curved - view obscured"
Straight
"Curved - view open"
Unknown

select distinct Crash_Road_Vert_Align from crash_locations;
"Curved - view obscured"
Straight
"Curved - view open"
Unknown

select count(distinct Crash_DCA_Code) from crash_locations;
-- 89 unique 3 digit codes


select distinct Crash_DCA_Description from crash_locations;
-- semi verbose description of crash scene, type of collision event.

select distinct Crash_DCA_Group_Description from crash_locations;
-- semi verbose description of DCA group.
-- one Crash_DCA_Group_Description covers multiple Crash_DCA_Description's.
select count(distinct Crash_DCA_Group_Description) from crash_locations;
-- 21 unique descriptions

select distinct DCA_Key_Approach_Dir from crash_locations;
S
E
N
W
""
U
P


select distinct Crash_Street, State_Road_Name, Loc_Suburb, Loc_Local_Government_Area, Loc_Post_Code
from crash_locations
limit 10;

select count(*) as count_, Crash_Street, State_Road_Name, Loc_Suburb, Loc_Local_Government_Area, Loc_Post_Code
from crash_locations
group by Crash_Street, State_Road_Name, Loc_Suburb, Loc_Local_Government_Area, Loc_Post_Code
limit 10;

select distinct Crash_Street from crash_locations;

select distinct Crash_Severity from crash_locations;
Hospitalisation
"Property damage only"
"Minor injury"
"Medical treatment"
Fatal


select distinct Crash_Nature from crash_locations;
Head-on
Angle
Rear-end
"Hit object"
Overturned
"Hit pedestrian"
Sideswipe
"Hit parked vehicle"
"Fall from vehicle"
"Non-collision - miscellaneous"
"Struck by external load"
"Collision - miscellaneous"
Other
"Hit animal"
"Struck by internal load"

select distinct Crash_Roadway_Feature from crash_locations;
"No Roadway Feature"
"Intersection - Cross"
"Intersection - T-Junction"
"Intersection - Roundabout"
"Intersection - Interchange"
Bridge/Causeway
"Median Opening"
"Intersection - Y-Junction"
"Intersection - Multiple Road"
"Merge Lane"
Bikeway
"Intersection - 5+ way"
Other
"Railway Crossing"
"Forestry/National Park Road"
Miscellaneous


select distinct Crash_Traffic_Control from crash_locations;
"No traffic control"
"Operating traffic lights"
"Give way sign"
"Flashing amber lights"
"Stop sign"
"Pedestrian crossing sign"
"Pedestrian operated lights"
Police
"LATM device"
"Road/Rail worker"
"Railway - lights and boom gate"
"Supervised school crossing"
Miscellaneous
"School crossing - flags"
"Railway - lights only"
"Railway crossing sign"
Other



.schema trafficcensus2020

CREATE TABLE IF NOT EXISTS "trafficcensus2020"(
  "SITE" TEXT,
  "DESCRIPTION" TEXT,
  "LONGITUDE" TEXT,
  "LATITUDE" TEXT,
  "THROUGH_DISTANCE" TEXT,
  "ROAD_SECTION_ID" TEXT,
  "ROAD_NAME" TEXT,
  "THROUGH_DISTANCE_START" TEXT,
  "THROUGH_DISTANCE_END" TEXT,
  "AADT" TEXT,
  "PC_CLASS_0A" TEXT,
  "PC_CLASS_0B" TEXT,
  "PC_CLASS_1A" TEXT,
  "PC_CLASS_1B" TEXT,
  "PC_CLASS_1C" TEXT,
  "PC_CLASS_1D" TEXT,
  "GROWTH_PC_1YR" TEXT,
  "GROWTH_PC_5YR" TEXT,
  "GROWTH_PC_10YR" TEXT,
  "PC_CLASS_2A" TEXT,
  "PC_CLASS_2B" TEXT,
  "PC_CLASS_2C" TEXT,
  "PC_CLASS_2D" TEXT,
  "PC_CLASS_2E" TEXT,
  "PC_CLASS_2F" TEXT,
  "PC_CLASS_2G" TEXT,
  "PC_CLASS_2H" TEXT,
  "PC_CLASS_2I" TEXT,
  "PC_CLASS_2J" TEXT,
  "PC_CLASS_2K" TEXT,
  "PC_CLASS_2L" TEXT,
  "REPORT_LINK" TEXT
);

/*
see page 3 of the reports for explanation of the PC_CLASS_xx columns.
2-Bin
0A Light vehicles
0B Heavy vehicles
4-Bin
1A Short vehicles
1B Truck or bus
1C Articulated vehicles
1D Road train
12-Bin
2A Short 2 axle vehicles
2B Short vehicles towing
2C 2 axle truck or bus
2D 3 axle truck or bus
2E 4 axle truck
2F 3 axle articulated vehicle
2G 4 axle articulated vehicle
2H 5 axle articulated vehicle
2I 6 axle articulated vehicle
2J B double
2K Double road train
2L Triple road train
*/

select distinct DESCRIPTION from trafficcensus2020;
select count(distinct DESCRIPTION) from trafficcensus2020;
-- 2237 sites.


select distinct PC_CLASS_0A from trafficcensus2020;


select DESCRIPTION, REPORT_LINK from trafficcensus2020 limit 5;


select
  max(LONGITUDE) as max_LONGITUDE,
  min(LONGITUDE) as min_LONGITUDE,
  max(LATITUDE) as max_LATITUDE,
  min(LATITUDE) as min_LATITUDE
from trafficcensus2020;
