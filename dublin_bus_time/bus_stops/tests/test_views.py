from django.test import TestCase
from django.urls import resolve
from bus_stops.views import Journey


class TestIndexView(TestCase):

    def test_resolve_to_test_get_index(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/')

        # check function name is equal
        self.assertEqual(found.func.__name__, Journey.as_view( ).__name__)

    def test_get_index(self):
        """test the get method"""
        # get url localhost:8000/
        response = self.client.get('/')

        # check which template is used
        self.assertTemplateUsed(response, 'index.html')

        # check response status is equal to 200
        self.assertEqual(response.status_code, 200)

    def test_prediction_only_walking(self):
        """test data from the post method can successfully predict the query with the case just walking"""
        prediction = Journey().resolve_data({"walking_data": [123], "bus_data": []}, 15)
        self.assertTrue(isinstance(prediction, int))

    def test_prediction_no_transfer(self):
        """test data from the post method can successfully predict the query without transfer"""
        prediction = Journey().resolve_data({"walking_data": [46, 827],
                                              "bus_data": [{"distance": 3700,
                                                            "route": "15", "duration": 668,
                                                            "departure": {"name": "Rathmines Garda Stn, stop 1170",
                                                                          "location": [53.3216895, -6.266525199999999],
                                                                          "timestamp": 1596435870000},
                                                            "arrival": {"name": "Eden Quay, stop 299",
                                                                        "location": [53.3482354, -6.2561569],
                                                                        "timestamp": 1596435870000}}]}, 15)

        self.assertTrue(isinstance(prediction, int))

    def test_prediction_with_transfer(self):
        """test data from the post method can successfully predict the query with transfer"""
        prediction = Journey().resolve_data({"walking_data": [180, 314, 28],
                                              "bus_data": [{"distance": 1487, "route": "145", "duration": 370,
                                                            "departure": {"name": "Arran Quay",
                                                                          "location": [53.3463411, -6.2785014],
                                                                          "timestamp": 1596448120000},
                                                            "arrival": {"name": "D'Olier Street",
                                                                        "location": [53.3465812, -6.2581256],
                                                                        "timestamp": 1596448120000}},
                                                           {"distance": 9216, "route": "130", "duration": 1281,
                                                            "departure": {"name": "Abbey Street, stop 7591",
                                                                          "location": [53.3489114, -6.2568793],
                                                                          "timestamp": 1596450081000},
                                                            "arrival": {"name": "Vernon Avenue, stop 1763",
                                                                        "location": [53.3644068, -6.1953694],
                                                                        "timestamp": 1596450081000}}]}, 15)

        self.assertTrue(isinstance(prediction, int))

    def test_prediction(self):
        """test the function can call the corresponding ml model to predict to journey"""
        prediction = Journey( ).journey_predict({"name": "Eden Quay, stop 299",
                                                 "location": [53.3482354, -6.2561569],
                                                 "timestamp": 1596435870000}, "15", 1, 15)
        self.assertTrue(isinstance(prediction, int))

    def test_stopid_mapping(self):
        """test the stopid can be get by given route and stop name"""
        stop_id = Journey().stop_id_mapping('83', 'Charlestown')
        self.assertEqual(stop_id, 1182)

    def test_progr_number_mapping(self):
        """test the prognumber can be get by given route and stopid"""
        prognumber = Journey().progr_number_mapping('67', '3907')
        self.assertEqual(prognumber, 57)

    def test_datetime_process(self):
        """test if the timestamp can successfully convert to different part of date time """
        hour, day_of_week, day_of_year, bank_holiday = Journey( ).datetime_process(1596445647000)
        self.assertEqual(hour, 9)
        self.assertEqual(day_of_week, 0)
        self.assertEqual(day_of_year, 216)
        self.assertEqual(bank_holiday, 0)

    def test_get_directions(self):
        """test if the direction can e inferenced by lat and lng"""
        direction = Journey().get_direction([53.3482354, -6.2561569], [53.3216895, -6.266525199999999])
        self.assertEqual(direction, 1)
