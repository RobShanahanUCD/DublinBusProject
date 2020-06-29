from django.urls import path, include
from . import views
from rest_framework import routers
from .models import BusStops

router = routers.DefaultRouter()
router.register('bus_stops', views.BusStopsListView, basename='bus_stops')

urlpatterns = [
    # path('bus_stops/<str:route>/', views.BusStopsListView.as_view()),
    path('predict/', views.Journey.as_view(), name="journey_predict"),
]
