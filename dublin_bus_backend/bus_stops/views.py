from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import BusStops
from .serializers import *


@api_view(['GET'])
def bus_stops_list(request):
    #Will be fed by request later on
    route = 14
    if request.method == 'GET':
        data = BusStops.objects.all().filter(route=route)
        serializer = BusStopsSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def journey_time(request):
    """Main function for our web app. Takes in the user information from the frontend.
    Passes this information into our model to generate an estimation for the journey time."""
    data = request.data
    try:
        #Will set up data processing module and model
        predictions = {
            'error': '0',
            'message': 'Successful',
            'prediction': 0
        }
    except Exception as e:
        predictions = {
            'error': '2',
            "message": str(e)
        }

    return Response(predictions, status=status.HTTP_201_CREATED)
