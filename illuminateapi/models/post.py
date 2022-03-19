from django.db import models
from django.db.models.deletion import CASCADE
from .appuser import AppUser


class Post(models.Model):
    author = models.ForeignKey(AppUser, on_delete=CASCADE, related_name='posts')
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(default=None)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    
    # CharField: chunk of space, not flexible, faster when smaller; 
    # TextField: rows can be smaller, no attribute
   
    @property
    def liked(self):
        return self.__liked
    
    @liked.setter
    def liked(self, value):
        self.__liked = value
        