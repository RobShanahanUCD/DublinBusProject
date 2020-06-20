# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Journey(models.Model):

    route = models.CharField(max_length=12)
    datetime = models.CharField(max_length=20)

    def __str__(self):
        return '{}, {}'.format(self.route, self.datetime)


class BusStops(models.Model):

    stopid = models.IntegerField(primary_key=True)
    stopname = models.CharField(max_length=60, blank=True, null=True)
    route = models.CharField(max_length=12)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    direction = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bus_stops'
        unique_together = (('stopid', 'route'),)


class FutureWeatherData(models.Model):
    number = models.IntegerField(blank=True, null=True)
    main = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    icon = models.CharField(max_length=45, blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    tempmin = models.FloatField(db_column='tempMin', blank=True, null=True)  # Field name made lowercase.
    tempmax = models.FloatField(db_column='tempMax', blank=True, null=True)  # Field name made lowercase.
    tempfeels = models.FloatField(db_column='tempFeels', blank=True, null=True)  # Field name made lowercase.
    humidity = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    windspeed = models.FloatField(db_column='windSpeed', blank=True, null=True)  # Field name made lowercase.
    winddeg = models.FloatField(db_column='windDeg', blank=True, null=True)  # Field name made lowercase.
    rain = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    day = models.CharField(max_length=45, blank=True, null=True)
    datetime = models.DateTimeField(db_column='dateTime', blank=True, null=True)  # Field name made lowercase.
    epoch = models.IntegerField()
    currdatetime = models.DateTimeField(db_column='currDateTime', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'future_weather_data'
        unique_together = (('currdatetime', 'epoch'),)


class LiveWeatherData(models.Model):
    number = models.IntegerField(blank=True, null=True)
    main = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    icon = models.CharField(max_length=45, blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    tempmin = models.FloatField(db_column='tempMin', blank=True, null=True)  # Field name made lowercase.
    tempmax = models.FloatField(db_column='tempMax', blank=True, null=True)  # Field name made lowercase.
    tempfeels = models.FloatField(db_column='tempFeels', blank=True, null=True)  # Field name made lowercase.
    humidity = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    windspeed = models.FloatField(db_column='windSpeed', blank=True, null=True)  # Field name made lowercase.
    winddeg = models.FloatField(db_column='windDeg', blank=True, null=True)  # Field name made lowercase.
    rain = models.FloatField(blank=True, null=True)
    sunrise = models.TimeField(blank=True, null=True)
    sunset = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    day = models.CharField(max_length=45, blank=True, null=True)
    datetime = models.DateTimeField(db_column='dateTime', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'live_weather_data'


class Weather(models.Model):
    dt = models.IntegerField(blank=True, null=True)
    dt_iso = models.TextField(blank=True, null=True)
    timezone = models.IntegerField(blank=True, null=True)
    city_name = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    feels_like = models.FloatField(blank=True, null=True)
    temp_min = models.FloatField(blank=True, null=True)
    temp_max = models.FloatField(blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    sea_level = models.TextField(blank=True, null=True)
    grnd_level = models.TextField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_deg = models.IntegerField(blank=True, null=True)
    rain_1h = models.TextField(blank=True, null=True)
    rain_3h = models.TextField(blank=True, null=True)
    snow_1h = models.TextField(blank=True, null=True)
    snow_3h = models.TextField(blank=True, null=True)
    clouds_all = models.IntegerField(blank=True, null=True)
    weather_id = models.IntegerField(blank=True, null=True)
    weather_main = models.TextField(blank=True, null=True)
    weather_description = models.TextField(blank=True, null=True)
    weather_icon = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
