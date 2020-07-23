from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dublin_bus_app/home.html')