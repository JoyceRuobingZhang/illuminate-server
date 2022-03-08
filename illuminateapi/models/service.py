from django.db import models

class Services(models.Model):
    # img
    name = models.CharField(max_length=55)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=6)
    longitude = models.DecimalField(max_digits=15, decimal_places=6)
    type = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    phone = models.CharField(max_length=25)
    rating = models.DecimalField(max_digits=15, decimal_places=6)
    sliding_scale = models.BooleanField(default=True)
    online = models.BooleanField(default=True)
        