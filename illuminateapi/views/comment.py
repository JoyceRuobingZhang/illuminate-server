"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from illuminateapi.models import Comment, AppUser, Post


class CommentView(ViewSet):
    """Category types"""
    
    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        comments = Comment.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def create(self, request):
        """Handle POST operations for comments

        Returns:
            Response -- JSON serialized comment instance
        """
        author = AppUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.author = author
        post_id = request.data["post_id"]
        post = Post.objects.get(id=post_id)
        comment.post = post
        comment.publication_date = request.data["publication_date"]
        comment.content = request.data["content"]
        
        if request.auth.user.is_staff:
            comment.approved = True

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Comment
        fields = ('id', 'content', 'publication_date', 'post', 'author') 
        depth = 2
        
