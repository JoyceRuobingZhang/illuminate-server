from django.db import models
from django.db.models.deletion import CASCADE
from .post import Post
from .appuser import AppUser


class Comment(models.Model):
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author = models.ForeignKey(AppUser, on_delete=CASCADE, related_name='comments')

