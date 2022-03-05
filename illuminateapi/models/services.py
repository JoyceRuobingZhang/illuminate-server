from unicodedata import category
from django.db import models
from django.db.models.deletion import CASCADE

class Services(models.Model):
    # img
    name = models.CharField(max_length=55)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    phone = models.CharField(max_length=25)
    rating = models.FloatField()
    
    # for custom properties that are not stored in the database
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        