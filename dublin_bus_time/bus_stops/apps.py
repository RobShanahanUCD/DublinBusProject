from django.apps import AppConfig


class BusStopsConfig(AppConfig):
    name = 'bus_stops'


class PredictionConfig(AppConfig):
    name = 'Prediction'
    # #CLASSIFIER_FOLDER = Path("classifier")
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # CLASSIFIER_FOLDER = os.path.join(BASE_DIR, 'Prediction/classifier/')
    # #CLASSIFIER_FILE = CLASSIFIER_FOLDER / "IRISRandomForestClassifier.joblib"
    # CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "IRISRandomForestClassifier.joblib")
    # classifier = load(CLASSIFIER_FILE)

