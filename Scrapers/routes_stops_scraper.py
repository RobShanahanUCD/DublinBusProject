import requests
from bs4 import BeautifulSoup as bs
import pymysql

host="MY_HOST"
port=3306
dbname="dublin_bus_time"
user="MY_USER"
password="MY_PASS"

conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
cursor = conn.cursor()
cursor1 = conn.cursor()

cursor.execute("select distinct stopid from bus_stops where name = 'bac'")

stops = cursor.fetchall()

stops = [list(i) for i in stops]
stops
for stop in stops:
    try:
        data = requests.get('https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=' + str(stop[0]))
        data = bs(data.text, 'html.parser')
        routes = data.find_all('label')
        for route in routes:
            label = route.get_text().strip()
            cursor.execute("""INSERT INTO routesstops (route, stopid) values(%s, %s)""",
                              (label, stop[0]))
            conn.commit()
    except:
        pass
            
            
    
        
    
