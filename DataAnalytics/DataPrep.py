import pymysql

localhost = "localhost"
user = 'MY_USER'
passwd = 'MY_PASS'
db = 'dublin_bus_time'
port = 3306

conn = pymysql.connect(host=localhost, user=user,
        passwd=passwd, db=db,
        port=port)
cursor = conn.cursor()

route = '77a'


cursor.execute("ALTER TABLE `dublin_bus_time`.`route_" + route + """` 
                ADD COLUMN `date` DATE NULL AFTER `LastUpdate`,
                ADD COLUMN `hour` INT NULL AFTER `date`,
                ADD COLUMN `temp` DOUBLE NULL AFTER `hour`,
                ADD COLUMN `wind_speed` DOUBLE NULL AFTER `temp`,
                ADD COLUMN `weather_main` VARCHAR(45) NULL AFTER `wind_speed`,
                ADD COLUMN `weather_description` VARCHAR(45) NULL AFTER `weather_main`,
                ADD COLUMN `morning_rush` VARCHAR(1) NULL AFTER `weather_description`,
                ADD COLUMN `evening_rush` VARCHAR(1) NULL AFTER `morning_rush`,
                ADD COLUMN `bank_holiday` VARCHAR(1) NULL AFTER `evening_rush`,
                ADD COLUMN `weekday` VARCHAR(3) NULL AFTER `bank_holiday`""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set date = str_to_date(left(DayOfService, 9), '%d-%M-%Y')""")
conn.commit()

cursor.execute("ALTER TABLE `dublin_bus_time`.`route_" + route + """` 
                CHANGE COLUMN `TripID` `TripID` VARCHAR(10) NOT NULL ,
                CHANGE COLUMN `StopPointID` `StopPointID` VARCHAR(6) NOT NULL ,
                CHANGE COLUMN `date` `date` DATE NOT NULL ,
                ADD PRIMARY KEY (`TripID`, `StopPointID`, `date`)""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set hour = least(hour(sec_to_time(ActualTime_Arr)), 23)""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """ b
                join dublin_bus_time.weather w on b.date = w.date and b.hour = w.hour 
                set b.temp = w.temp, b.wind_speed = w.wind_speed, b.weather_main = w.weather_main, b.weather_description = w.weather_description""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set morning_rush = 'N'""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set morning_rush = 'Y'
                where hour in (7, 8, 9)""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set evening_rush = 'N'""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set evening_rush = 'Y'
                where hour in (16, 17, 18)""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """
                set bank_holiday = 'N'""")
conn.commit()

cursor.execute("update dublin_bus_time.route_" + route + """ b
                join dublin_bus_time.bank_holidays h on b.date = h.date
                set b.bank_holiday = 'Y'""")
conn.commit()

cursor.close()
conn.close()

