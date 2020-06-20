# Generated by Django 3.0.7 on 2020-06-19 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStops',
            fields=[
                ('stopid', models.IntegerField(primary_key=True, serialize=False)),
                ('stopname', models.CharField(blank=True, max_length=60, null=True)),
                ('route', models.CharField(max_length=12)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('direction', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bus_stops',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FutureWeatherData',
            fields=[
                ('number', models.IntegerField(blank=True, null=True)),
                ('main', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=45, null=True)),
                ('icon', models.CharField(blank=True, max_length=45, null=True)),
                ('temp', models.FloatField(blank=True, null=True)),
                ('tempmin', models.FloatField(blank=True, db_column='tempMin', null=True)),
                ('tempmax', models.FloatField(blank=True, db_column='tempMax', null=True)),
                ('tempfeels', models.FloatField(blank=True, db_column='tempFeels', null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('pressure', models.FloatField(blank=True, null=True)),
                ('windspeed', models.FloatField(blank=True, db_column='windSpeed', null=True)),
                ('winddeg', models.FloatField(blank=True, db_column='windDeg', null=True)),
                ('rain', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('day', models.CharField(blank=True, max_length=45, null=True)),
                ('datetime', models.DateTimeField(blank=True, db_column='dateTime', null=True)),
                ('epoch', models.IntegerField()),
                ('currdatetime', models.DateTimeField(db_column='currDateTime', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'future_weather_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LiveWeatherData',
            fields=[
                ('number', models.IntegerField(blank=True, null=True)),
                ('main', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=45, null=True)),
                ('icon', models.CharField(blank=True, max_length=45, null=True)),
                ('temp', models.FloatField(blank=True, null=True)),
                ('tempmin', models.FloatField(blank=True, db_column='tempMin', null=True)),
                ('tempmax', models.FloatField(blank=True, db_column='tempMax', null=True)),
                ('tempfeels', models.FloatField(blank=True, db_column='tempFeels', null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('pressure', models.FloatField(blank=True, null=True)),
                ('windspeed', models.FloatField(blank=True, db_column='windSpeed', null=True)),
                ('winddeg', models.FloatField(blank=True, db_column='windDeg', null=True)),
                ('rain', models.FloatField(blank=True, null=True)),
                ('sunrise', models.TimeField(blank=True, null=True)),
                ('sunset', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('day', models.CharField(blank=True, max_length=45, null=True)),
                ('datetime', models.DateTimeField(db_column='dateTime', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'live_weather_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.IntegerField(blank=True, null=True)),
                ('dt_iso', models.TextField(blank=True, null=True)),
                ('timezone', models.IntegerField(blank=True, null=True)),
                ('city_name', models.TextField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('temp', models.FloatField(blank=True, null=True)),
                ('feels_like', models.FloatField(blank=True, null=True)),
                ('temp_min', models.FloatField(blank=True, null=True)),
                ('temp_max', models.FloatField(blank=True, null=True)),
                ('pressure', models.IntegerField(blank=True, null=True)),
                ('sea_level', models.TextField(blank=True, null=True)),
                ('grnd_level', models.TextField(blank=True, null=True)),
                ('humidity', models.IntegerField(blank=True, null=True)),
                ('wind_speed', models.FloatField(blank=True, null=True)),
                ('wind_deg', models.IntegerField(blank=True, null=True)),
                ('rain_1h', models.TextField(blank=True, null=True)),
                ('rain_3h', models.TextField(blank=True, null=True)),
                ('snow_1h', models.TextField(blank=True, null=True)),
                ('snow_3h', models.TextField(blank=True, null=True)),
                ('clouds_all', models.IntegerField(blank=True, null=True)),
                ('weather_id', models.IntegerField(blank=True, null=True)),
                ('weather_main', models.TextField(blank=True, null=True)),
                ('weather_description', models.TextField(blank=True, null=True)),
                ('weather_icon', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weather',
                'managed': False,
            },
        ),
    ]
