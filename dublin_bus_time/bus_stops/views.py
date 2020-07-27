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
from rest_framework.renderers import TemplateHTMLRenderer


sys.path.append(os.getcwd())
from .ml_models import train_model as ml


def stop_id_mapping(route, stop_name):
    stop_id = BusNameHashmap.cache[(route, stop_name)]
    return stop_id


def progr_number_mapping(route, stop_id):
    progr_number = BusStopHashmap.cache[(route, stop_id)]
    return progr_number


def datetime_process(data):
    hour, day_of_week, day_of_year, bank_holiday = 20, 3, 100, 0
    return hour, day_of_week, day_of_year, bank_holiday


def journey_predict(data):
    hour, day_of_week, day_of_year, bank_holiday = datetime_process(data['datetime'])
    route = data['route']
    direction = data['direction']

    if len(data['stop_id'].split(',')) < 2:
        stop_name = data['stop_id'].split(',')[0]
        stop_id = stop_id_mapping(stop_name)
    else:
        stop_id = data['stop_id'].split(',')[1].split(" ")[-1]

    progrnumber = progr_number_mapping(route, stop_id)
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

    x_input_df = ml.ModelTraining( ).time_transform(x_input_df, 'day_of_week', 7)
    x_input_df = ml.ModelTraining( ).time_transform(x_input_df, 'hour', 24)

    path = 'route_' + route + '__lgbm_model.pkl'
    model_path = os.path.join(PredictionConfig.MODELS_FOLDER, path)
    ml_model = joblib.load(model_path)
    y_prediction = ml_model.predict(x_input_df)
    return y_prediction[0]


class BusStopsListView(generics.ListAPIView):
    serializer_class = BusStopsSerializer

    def get_queryset(self):
        route = self.kwargs['route']
        queryset = BusStops.objects
        data = queryset.filter(route=route)
        return data


class Journey(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = './templates/index.html'

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        """Main function for our web app. Takes in the user information from the frontend.
        Passes this information into our model to generate an estimation for the journey time."""
        data = request.data
        prediction = journey_predict(data)

        predictions = {"PredicedJourneyTime": prediction}
        return render(request, 'index.html', predictions)
