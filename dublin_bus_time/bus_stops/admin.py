from django.contrib import admin
from .models import BusStops, FutureWeatherData, LiveWeatherData, Weather, Journey, Timetable


admin.site.register(BusStops)
admin.site.register(FutureWeatherData)
admin.site.register(LiveWeatherData)
admin.site.register(Weather)
admin.site.register(Journey)
admin.site.register(Timetable)



