from datetime import datetime

import json
import pymysql
import requests
import time

try:
	host="MY_DATABASE"
	port=3306
	dbname="dublin_bus_static"
	user="MY_USER"
	password="MY_PASSWORD"

	conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
	cursor = conn.cursor()

	#makes call to api
	ID = '7778677'
	APPID = 'MY_API_KEY'
	WEATHER_URI = "http://api.openweathermap.org/data/2.5/forecast"
	UNITS = "metric"
	response = requests.get(WEATHER_URI, params={"id": ID, "appid": APPID, "units": UNITS})

	data = response.text
	parsed = json.loads(data)

	for x in range(len(parsed["list"])):

		number = parsed["list"][x]["weather"][0]["id"]
		main = parsed["list"][x]["weather"][0]["main"]
		description = parsed["list"][x]["weather"][0]["description"]
		icon =  parsed["list"][x]["weather"][0]["icon"]
		temp =  round(int(parsed["list"][x]["main"]["temp"]))
		tempMin =  round(int(parsed["list"][x]["main"]["temp_min"]))
		tempMax =  round(int(parsed["list"][x]["main"]["temp_max"]))
		tempFeels =  round(int(parsed["list"][x]["main"]["feels_like"]))
		pressure =  parsed["list"][x]["main"]["pressure"]
		humidity =  parsed["list"][x]["main"]["humidity"]
		windSpeed =  parsed["list"][x]["wind"]["speed"]
		windDeg =  parsed["list"][x]["wind"]["deg"]
		try:
			rain = parsed["list"][x]["rain"]["1h"]
		except:
			rain = 0
		epoch = (parsed["list"][x]["dt"])
		year = time.strftime("%Y", time.localtime(epoch))
		month = time.strftime("%m", time.localtime(epoch))
		date = time.strftime("%d", time.localtime(epoch))
		dateUpdate = year+"-"+month+"-"+date
		timeUpdate = time.strftime("%H:%M:%S", time.localtime(epoch))
		dateTime = dateUpdate + " " + timeUpdate
		dayUpdate = time.strftime("%a", time.localtime(epoch))
		now = datetime.now()
		currDateTime = now.strftime("%Y/%m/%d %H:%M:%S")

		#checks for duplicate row on database and if it is then it skips
		# noinspection PyBroadException,PyBroadException
		try:
			#pushes data to SQL table on database
			cursor.execute("INSERT INTO future_weather_data (number, main, description, icon, temp, tempMin, tempMax, tempFeels, humidity, pressure, windSpeed, windDeg, rain, date, time, day, dateTime, epoch, currDateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",(number,main,description,icon,temp,tempMin,tempMax,tempFeels,humidity,pressure,windSpeed,windDeg,rain,dateUpdate,timeUpdate,dayUpdate,dateTime,epoch,currDateTime))
			conn.commit()
		except:
			pass

	conn.close()

except:
	pass
