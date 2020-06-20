from django.urls import path, include
from . import views
from rest_framework import routers
from .models import BusStops

router = routers.DefaultRouter()
router.register('bus_stops', views.BusStopsListView, basename='bus_stops')

urlpatterns = [
    # path('journey_time/', views.Journey.as_view(), name="journey_time"),
    path('bus_stops/<str:route>/', views.BusStopsListView.as_view()),
    path('time/', views.journey_predict),
    path('form/', views.UserForm.as_view(), name="journey_form"),
]
