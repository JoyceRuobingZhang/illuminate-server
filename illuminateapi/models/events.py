from unicodedata import category
from django.db import models
from django.db.models.deletion import CASCADE
from .appuser import AppUser
from .categories import Category
from illuminateapi.models import appuser



class Event(models.Model):
    # img
    name = models.CharField(max_length=55)
    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    host = models.CharField(max_length=50)
    created_by = models.ForeignKey(AppUser, on_delete=CASCADE, related_name='created_events') # alias event_set
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name='events')
    
    # for custom properties that are not stored in the database
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        
        

    
    
   