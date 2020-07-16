from sqlalchemy import create_engine
import pandas as pd
from dublin_bus_time.bus_stops.ml_models.all_route import RouteList
import os

def make_pickle(route):
    route_data = pd.read_sql_table(table_name=route, schema="dublin_bus_time", con=engine)
    # bank_holidays = pd.read_sql_table(table_name="bank_holidays", schema="dublin_bus_time", con=engine)
    # weather = pd.read_sql_table(table_name="weather", schema="dublin_bus_time", con=engine)

    path = "./" + route + "__.pkl"
    print(path)
    route_data.to_pickle(path)
    # bank_holidays.to_pickle("./bank_holidays__.pkl")
    # weather.to_pickle("./weather__.pkl")
    print(route, " pickle built!!")

if __name__ == '__main__':
    host = '127.0.0.1'
    username = 'root'
    password = '29336629'
    database = 'dublin_bus_time'
    URI = f'mysql+pymysql://{username}:{password}@{host}/{database}'

    routes = RouteList().route_list
    routes_set = set(routes)

    engine = create_engine(URI, convert_unicode=True, echo=False)

    for route in routes:
        if route not in routes_set: continue
        route_path = "route_" + route
        if os.path.isfile("./" + route_path + "__.pkl"): continue
        print(route_path)
        make_pickle(route_path)
