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


        data = request.data
        bus_journey_time = 0
        for step in data['bus_data']:
            try:
                direction = self.get_direction(step['arrival']['location'], step['departure']['location'])
                bus_journey_time += (self.journey_predict(step['arrival'], step['route'], direction) -
                                     self.journey_predict(step['departure'], step['route'], direction))
            except Exception as e:
                print("Error", e)
                bus_journey_time += step['duration']
        walking_time = sum(data['walking_data'])
        prediction = bus_journey_time + walking_time
        predictions = {"PredicedJourneyTime": prediction}
        return Response(predictions, status=status.HTTP_200_OK)

    def stop_id_mapping(self, route, stop_name):
        stop_id = BusNameHashmap.cache[(route, stop_name)]
        return stop_id

    def progr_number_mapping(self, route, stop_id):
        print("route:", route, "stop_id:", stop_id)
        progr_number = BusStopHashmap.cache[(route, stop_id)]
        return progr_number

    def datetime_process(self, timestamp):
        hour = pd.to_datetime(timestamp, unit='ms').hour
        day_of_week = pd.to_datetime(timestamp, unit='ms').dayofweek
        day_of_year = pd.to_datetime(timestamp, unit='ms').dayofyear
        bank_holiday_set = {1, 76, 103, 124, 152, 215, 299, 359, 360}
        bank_holiday = 1 if day_of_year in bank_holiday_set else 0
        return hour, day_of_week, day_of_year, bank_holiday

    def get_direction(self, arrival, departure):
        # IB = inbound / going / northbound / eastbound 1
        # OB = outbound / back / southbound / westbound 2
        lat_diff = arrival[0] - departure[0]
        lng_diff = arrival[1] - departure[1]
        if abs(lat_diff) >= abs(lng_diff):
            direction = 1 if lat_diff > 0 else 2
        else:
            direction = 1 if lng_diff > 0 else 2
        return direction

    def journey_predict(self, data, route, direction):

        hour, day_of_week, day_of_year, bank_holiday = self.datetime_process(data['timestamp'])
        print(data['name'])

        if "stop" in data['name']:
            print(data['name'].split('stop')[-1].strip())
            stop_id = str(data['name'].split('stop')[-1].strip())
            print(stop_id, type(stop_id))
        else:
            print(data['name'].split(','))
            stop_name = data['name'].strip()
            stop_id = str(self.stop_id_mapping(route, stop_name))
            print(stop_id)

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
        x_input_df['StopPointID'] = x_input_df['StopPointID'].astype('category')
        path = 'route_' + route + '__lgbm_model.pkl'
        model_path = os.path.join(PredictionConfig.MODELS_FOLDER, path)
        ml_model = joblib.load(model_path)
        y_prediction = ml_model.predict(x_input_df)
        print("prediction", y_prediction[0])
        return y_prediction[0]

