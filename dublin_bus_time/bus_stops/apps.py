from django.apps import AppConfig
import os


class BusStopsConfig(AppConfig):
    name = 'bus_stops'


class PredictionConfig(AppConfig):
    name = 'Prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODELS_FOLDER = os.path.join(BASE_DIR, 'bus_stops/ml_models/')
