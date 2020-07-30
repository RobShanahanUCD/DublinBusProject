import requests
from bs4 import BeautifulSoup as bs
import pymysql


host="MY_HOST"
port=3306
dbname="MY_DATABASE"
user="MYUSER"
password="MY_PASSWORD"

conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
cursor = conn.cursor()



data = requests.get('https://www.dublinbus.ie/Your-Journey1/Timetables/')

data = bs(data.text, 'html.parser')

routes = data.find_all('a', {'title': 'Read more'})

for route in routes:
    # noinspection PyBroadException
    try:
        
        innerHTML = route.get_text().strip()
        link = 'https://www.dublinbus.ie' + route.attrs['href']
        timetable = requests.get(link)
        timetable = bs(timetable.text, 'html.parser')
        display = timetable.find_all('div', {'class':'timetable_horiz_display'})
        origin = display[0].find_all('div', {'class':'TT_Title_left'})[0].contents[2].strip()
        days = display[1].find_all('div', {'class':'timetable_sheet_holder'})
        for day in days:
            weekday = day.find_all('span')[0].get_text().strip()
            times = day.find_all('div', {'class':'time'})
            for time in times:
                value = time.get_text().strip()
                cursor.execute("""INSERT INTO timetable (route, origin, days, time) values(%s, %s, %s, %s)""",
                              (innerHTML, origin, weekday, value))
                conn.commit()


        origin = display[3].find_all('div', {'class':'TT_Title_left'})[0].contents[2].strip()
        days = display[4].find_all('div', {'class':'timetable_sheet_holder'})        
        for day in days:
            weekday = day.find_all('span')[0].get_text().strip()
            times = day.find_all('div', {'class':'time'})
            for time in times:
                value = time.get_text().strip()
                cursor.execute("""INSERT INTO timetable (route, origin, days, time) values(%s, %s, %s, %s)""",
                              (innerHTML, origin, weekday, value))
                conn.commit()
    except:
        pass
    
    
conn.close
