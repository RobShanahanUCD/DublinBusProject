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
        walking, bus = self.json_extraction(data)
        print(bus)
        # prediction = self.journey_predict(data)
        prediction = bus
        predictions = {"PredicedJourneyTime": prediction}
        return Response(predictions, status=status.HTTP_200_OK)

    def json_extraction(self, data):
        filtered_data = 0
        walking = list()
        bus = list()
        for step in data:
            if step['travel_mode'] == "WALKING":
                walking.append({"duration": step["duration"].get("value", 0)})
            elif step['travel_mode'] == "TRANSIT":
                bus.append({"duration": step["duration"].get("value", 0,),
                            "distance": step["distance"].get("value", 0,),
                            "arrival_stop": step["transit"]["arrival_stop"].get("name", None),
                            "arrival_time": step["transit"]["arrival_time"].get("value", None),
                            "departure_stop": step["transit"]["departure_stop"].get("name", None),
                            "departure_time": step["transit"]["departure_time"].get("value", None)
                            })

        return walking, bus

    def stop_id_mapping(self, route, stop_name):
        stop_id = BusNameHashmap.cache[(route, stop_name)]
        return stop_id

    def progr_number_mapping(self, route, stop_id):
        progr_number = BusStopHashmap.cache[(route, stop_id)]
        return progr_number

    def datetime_process(self, data):
        hour, day_of_week, day_of_year, bank_holiday = 20, 3, 100, 0
        return hour, day_of_week, day_of_year, bank_holiday

    def journey_predict(self, data):
        hour, day_of_week, day_of_year, bank_holiday = self.datetime_process(data['datetime'])
        route = data['route']
        direction = data['direction']

        if len(data['stop_id'].split(',')) < 2:
            stop_name = data['stop_id'].split(',')[0]
            stop_id = self.stop_id_mapping(stop_name)
        else:
            stop_id = data['stop_id'].split(',')[1].split(" ")[-1]

        progrnumber = self.progr_number_mapping(route, stop_id)
        temp = data['temp']

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

