from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .models import BusStops
from .serializers import *

#Using class based view extended from APIView
class BusStopsList(APIView):
    def get(self, request, *args, **kwargs):
        route = self.kwargs['route']
        if request.method == 'GET':
            data = BusStops.objects.all().filter(route=route)
            serializer = BusStopsSerializer(data, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class Journey(APIView):
    def post(self, request, *args, **kwargs):
        """Main function for our web app. Takes in the user information from the frontend.
        Passes this information into our model to generate an estimation for the journey time."""
        data = request.data
        try:
            # Will set up data processing module and model
            data = request.data
            prediction = 100000
            predictions = {
                'error': '0',
                'message': 'Successful',
                'prediction': prediction
            }
        except Exception as e:
            predictions = {
                'error': '2',
                "message": str(e)
            }

        return Response(predictions, status=status.HTTP_201_CREATED)
