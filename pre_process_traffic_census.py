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
from config import *

input_fn_traffic_census = INPUT_FN_TRAFFIC_CENSUS
df_traffic_census = pd.read_csv(input_fn_traffic_census)
print("df_traffic_census.shape:", df_traffic_census.shape)
df_traffic_census.columns



df = pd.read_json("data/qld_traffic_survey_codes.json")
