from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework import generics
import joblib
from .bus_stop_hashmap import BusStopHashmap
from .apps import PredictionConfig
import os
import sys
import pandas as pd

sys.path.append(os.getcwd())
from .ml_models import train_model as ml


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
    stop_id = data['stop_id']

    progrnumber = progr_number_mapping(route, stop_id)
    temp = data['temp']

    x_input = {
        'ProgrNumber': [progrnumber],
        'Direction': [int(direction)],
        'bank_holiday': [int(bank_holiday)],
        'temp': [float(temp)],
        'day_of_year': [day_of_year],
        'day_of_week': [day_of_week],
        'hour': [hour]
    }
    x_input_df = pd.DataFrame(x_input)

    x_input_df = ml.ModelTraining().time_transform(x_input_df, 'day_of_week', 7)
    x_input_df = ml.ModelTraining().time_transform(x_input_df, 'hour', 24)

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
    def post(self, request):
        """Main function for our web app. Takes in the user information from the frontend.
        Passes this information into our model to generate an estimation for the journey time."""
        data = request.data
        prediction = journey_predict(data)
        # prediction_model = PredictionConfig.classifier

        predictions = {"PredicedJourneyTime": prediction}
        return Response(predictions, status=status.HTTP_200_OK)
