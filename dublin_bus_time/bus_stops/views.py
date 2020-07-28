from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework import generics
import joblib
from .bus_name_hashmap import BusNameHashmap
from .prog_number_hashmap import BusStopHashmap
from .apps import PredictionConfig
import os
import sys
import pandas as pd
from django.shortcuts import render
import pprint

sys.path.append(os.getcwd())
from .ml_models import train_model as ml


class BusStopsListView(generics.ListAPIView):
    serializer_class = BusStopsSerializer

    def get_queryset(self):
        route = self.kwargs['route']
        queryset = BusStops.objects
        data = queryset.filter(route=route)
        return data


class Journey(APIView):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        """Main function for our web app. Takes in the user information from the frontend.
        Passes this information into our model to generate an estimation for the journey time."""

        # IB = inbound / going / northbound / eastbound 1
        # OB = outbound / back / southbound / westbound 2
        data = request.data
        bus_journey_time = 0
        for step in data['bus_data']:
            try:
                bus_journey_time += (self.journey_predict(step['arrival'], step['route']) -
                                     self.journey_predict(step['departure'], step['route']))
            except Exception as e:
                print(e)
                bus_journey_time += step['duration']
        walking_time = sum(data['walking_data'])
        prediction = bus_journey_time + walking_time
        predictions = {"PredicedJourneyTime": prediction}
        return Response(predictions, status=status.HTTP_200_OK)

    def stop_id_mapping(self, route, stop_name):
        stop_id = BusNameHashmap.cache[(route, stop_name)]
        return stop_id

    def progr_number_mapping(self, route, stop_id):
        progr_number = BusStopHashmap.cache[(route, stop_id)]
        return progr_number

    def datetime_process(self, timestamp):
        hour = pd.to_datetime(timestamp, unit='ms').hour
        day_of_week = pd.to_datetime(timestamp, unit='ms').dayofweek
        day_of_year = pd.to_datetime(timestamp, unit='ms').dayofyear
        bank_holiday_set = {1, 76, 103, 124, 152, 215, 299, 359, 360}
        bank_holiday = 1 if day_of_year in bank_holiday_set else 0
        return hour, day_of_week, day_of_year, bank_holiday

    def get_direction(self, ):

    def journey_predict(self, data, route):

        hour, day_of_week, day_of_year, bank_holiday = self.datetime_process(data['timestamp'])

        direction = data['direction']

        if len(data['stop_id'].split(',')) < 2:
            stop_name = data['stop_id'].split(',')[0]
            stop_id = self.stop_id_mapping(stop_name)
        else:
            stop_id = data['stop_id'].split(',')[1].split(" ")[-1]

        progrnumber = self.progr_number_mapping(route, stop_id)
        # temp = data['temp']
        temp = 20
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

        x_input_df = ml.ModelTraining().time_transform(x_input_df, 'day_of_week', 7)
        x_input_df = ml.ModelTraining().time_transform(x_input_df, 'hour', 24)

        path = 'route_' + route + '__lgbm_model.pkl'
        model_path = os.path.join(PredictionConfig.MODELS_FOLDER, path)
        ml_model = joblib.load(model_path)
        y_prediction = ml_model.predict(x_input_df)
        return y_prediction[0]

