from sqlalchemy import create_engine
import pandas as pd
import joblib
import json


host = 'dublinbus.cegwluuehipg.eu-west-1.rds.amazonaws.com'
username = 'admin'
password = 'robpaijohn'
database = 'dublin_bus_static'
URI = f'mysql+pymysql://{username}:{password}@{host}/{database}'

engine = create_engine(URI, convert_unicode=True, echo=False)
routesstops = pd.read_sql_table(table_name='routesstops', schema="dublin_bus_static", con=engine)

routesstops_cache = dict()

for index, row in routesstops.iterrows():
    routesstops_cache[(row['route'], row['stopid'])] = row['progr_number']

# joblib.dump(routesstops_cache, "bus_stop_map.pkl")
# routesstops_cache = joblib.load("bus_stop_map.pkl")
# print(routesstops_cache)

with open('bus_stop_hashmap.txt', 'w') as f:
    f.write(routesstops_cache)

