from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .models import BusStops
from .serializers import *
from .apps import PredictionConfig
from .forms import JourneyForm
from django.contrib import messages
from rest_framework import generics

def journey_predict(data):
    return int(data['route']) + int(data['time'])


class BusStopsListView(generics.ListAPIView):
    serializer_class = BusStopsSerializer

    def get_queryset(self):
        route = self.kwargs['route']
        queryset = BusStops.objects
        data = queryset.filter(route=route)
        return data


# # Using class based view extended from APIView
# class BusStopsList(APIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     def get(self, request, *args, **kwargs):
#         route = self.kwargs['route']
#         if request.method == 'GET':
#             data = BusStops.objects.all().filter(route=route).distinct()
#             serializer = BusStopsSerializer(data, context={'request': request}, many=True)
#             return render(request, 'index.html', {"context": serializer.data}, status=status.HTTP_200_OK)
#             # return Response(serializer.data, status=status.HTTP_200_OK, template_name='index.html')


class UserForm(APIView):
    def post(self, request):
        if request.method == 'POST':
            form = JourneyForm(request.POST)
            if form.is_valid():
                route = form.cleaned_data['route']
                time = form.cleaned_data['time']
                data = (request.POST).dict()
                answer = journey_predict(data)
                messages.success(request, 'Time: {}'.format(answer))
        form = JourneyForm()
        return render(request, 'index.html', {'form': form})


# class Journey(APIView):
#     def post(self, request):
#         """Main function for our web app. Takes in the user information from the frontend.
#         Passes this information into our model to generate an estimation for the journey time."""
#         data = request.data
#         # prediction_model = PredictionConfig.classifier
#         total = 0
#         for k, v in data.items():
#             total += v
#
#         predictions = {"Prediced Journey Time": total}
#         return Response(predictions, status=status.HTTP_201_CREATED)
