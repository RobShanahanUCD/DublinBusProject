from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bus_stops', views.BusStopsListView, basename='bus_stops')

urlpatterns = [
    path('', views.Journey.as_view(), name="index"),
    path('predict/', views.Journey.as_view(), name="journey_predict"),
    path('timetable/', views.GetTimetable.as_view(), name="timetable_data"),
    #path('RealTimeInformation/', views.GetTimetable.as_view(), name="RTI"),
]
