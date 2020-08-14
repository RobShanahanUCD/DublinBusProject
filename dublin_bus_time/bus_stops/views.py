import os
import sys
import pandas as pd
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import *
import joblib
from .bus_name_hashmap import BusNameHashmap
from .prog_number_hashmap import BusStopHashmap
from .apps import PredictionConfig
from django.shortcuts import render
from .models import LiveWeatherData
from .models import Timetable
from django.views.generic import TemplateView, DetailView, ListView


sys.path.append(os.getcwd( ))
from .ml_models import train_model as ml


class BusStopsListView(generics.ListAPIView):
    """Get the bus stops in database, not for production use"""

    serializer_class = BusStopsSerializer

    def get_queryset(self):
        """get the bus stop in a route"""
        route = self.kwargs['route']
        queryset = BusStops.objects
        data = queryset.filter(route=route)
        return data


class Journey(APIView):
    """Main functionality in this REST API"""

    def get(self, request):
        """render the page when loaded"""
        return render(request, 'index.html')

    def post(self, request):
        """Main function for our web app. Takes in the user information from the frontend.
        Passes this information into our model to generate an estimation for the journey time."""

        data = request.data
        # Get temp data from live weather database
        queryset = LiveWeatherData.objects.order_by('-datetime').values()[0]
        temp = queryset['temp']
        predictions = {"PredictedJourneyTime": self.resolve_data(data, temp)}
        return Response({"PredictedJourneyTime": predictions}, status=status.HTTP_200_OK)

    def resolve_data(self, data, temp):

        bus_journey_time = 0
        google_map_reference = 0

        # Predict all the segment of bus trip
        if len(data['bus_data']) > 0:
            for step in data['bus_data']:
                google_map_reference += step['duration']
                try:
                    direction = self.get_direction(step['arrival']['location'], step['departure']['location'])
                    bus_journey_time += abs((self.journey_predict(step['arrival'], step['route'], direction, temp) -
                                             self.journey_predict(step['departure'], step['route'], direction, temp)))

                # If prediction fails, use the prediction from google map
                except Exception as e:
                    print("Error", e)
                    bus_journey_time += step['duration']

        walking_time = sum(data['walking_data'])
        prediction = bus_journey_time + walking_time
        # For studying the error of our prediction to the google map
        # error_rate = abs(bus_journey_time - google_map_reference) / google_map_reference
        # print('Error rate: ', error_rate)
        return prediction

    def stop_id_mapping(self, route, stop_name):
        """Get the stop id from route and stop name"""
        stop_id = BusNameHashmap.cache[(route, stop_name)]
        return stop_id

    def progr_number_mapping(self, route, stop_id):
        """Get the progr number from route and stop id"""
        progr_number = BusStopHashmap.cache[(route, stop_id)]
        return progr_number

    def datetime_process(self, timestamp):
        """Convert the timestamp to different  part of date time"""
        hour = pd.to_datetime(timestamp, unit='ms').hour
        day_of_week = pd.to_datetime(timestamp, unit='ms').dayofweek
        day_of_year = pd.to_datetime(timestamp, unit='ms').dayofyear
        # Bank holiday day of year in 2002
        bank_holiday_set = {1, 76, 103, 124, 152, 215, 299, 359, 360}
        bank_holiday = 1 if day_of_year in bank_holiday_set else 0
        return hour, day_of_week, day_of_year, bank_holiday

    def get_direction(self, arrival, departure):
        """Use lat and lng to inference the direction of bus, can be inaccurate sometimes, just a workaround"""
        # IB = inbound / going / northbound / eastbound 1
        # OB = outbound / back / southbound / westbound 2
        lat_diff = arrival[0] - departure[0]
        lng_diff = arrival[1] - departure[1]
        if abs(lat_diff) >= abs(lng_diff):
            direction = 1 if lat_diff > 0 else 2
        else:
            direction = 1 if lng_diff > 0 else 2
        return direction

    def journey_predict(self, data, route, direction, temp):
        """Calculate the journey time by lgbm machine learning model"""
        hour, day_of_week, day_of_year, bank_holiday = self.datetime_process(data['timestamp'])

        # Sometimes the Google Directions api doesn't have stop id, if there is extract them from the stop name
        if "stop" in data['name']:
            # print(data['name'].split('stop')[-1].strip())
            stop_id = str(data['name'].split('stop')[-1].strip( ))
            # print(stop_id, type(stop_id))
        else:
            stop_name = data['name'].strip()
            stop_id = str(self.stop_id_mapping(route, stop_name))
            # print(stop_id, type(stop_id))

        progrnumber = self.progr_number_mapping(route, stop_id)
        x_input = {
            'ProgrNumber': [progrnumber],
            'Direction': [int(direction)],
            'hour': [hour],
            'StopPointID': [stop_id],
            'bank_holiday': [int(bank_holiday)],
            'temp': [float(temp)],
            'day_of_year': [day_of_year],
            'day_of_week': [day_of_week],
        }
        x_input_df = pd.DataFrame(x_input)

        # ML model data pre-processing
        x_input_df = ml.ModelTraining().time_transform(x_input_df, 'day_of_week', 7)
        x_input_df = ml.ModelTraining().time_transform(x_input_df, 'hour', 24)
        x_input_df['StopPointID'] = x_input_df['StopPointID'].astype('category')

        path = 'route_' + route.upper() + '__lgbm_model.pkl'
        model_path = os.path.join(PredictionConfig.MODELS_FOLDER, path)
        ml_model = joblib.load(model_path)
        y_prediction = ml_model.predict(x_input_df)
        return int(y_prediction[0])


class GetTimetable(ListView):
    context_object_name = 'timetable_data'
    template_name = 'timetable.html'

    def get_queryset(self, **kwargs):
        queryset = Timetable.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['distinct'] = Timetable.objects.values('route', 'origin').distinct()
        return context
        #return {'QuerySet':QuerySet, 'distinct':distinct}
        #return render(request, "timetable.html", {'time_data': QuerySet})
        


    
