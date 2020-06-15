from django.db import models

class BusStops(models.Model):
    name = models.CharField(max_length=60)
    stopID = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    registrationDate = models.DateField("Registration Date", auto_now_add=True)

    def __str__(self):
        return self.name
