from django.db import models


class Geodata(models.Model):
    """
    This is a simple model that stores
    physical coordinates and
    address points on the map.
    """

    latitude = models.FloatField(max_length=20, verbose_name='Latitude')
    longitude = models.FloatField(max_length=20, verbose_name='Longitude')
    address = models.TextField(verbose_name='Address')

    def getObject(self):
        return {
            'lat': self.latitude,
            'lng': self.longitude,
            'address': self.address
        }
