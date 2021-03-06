"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from illuminateapi.models import Post, AppUser


class PostView(ViewSet):
    """One Post"""

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        author = AppUser.objects.get(user=request.auth.user)

        post = Post()
        post.author = author
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        
        if request.auth.user.is_staff:
            post.approved = True

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        appuser = AppUser.objects.get(user=request.auth.user)

        for post in posts:
            post.liked = appuser in post.liked_by.all()
        
        # filter
        authorId = self.request.query_params.get('authorId', None)
        
        if authorId is not None:
            posts = posts.filter(author__id=authorId)
       
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
    

    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        author = AppUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)        
        post.author = author
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]

        post.save()
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        author = AppUser.objects.get(user=request.auth.user)

        
        try:
            post = Post.objects.get(pk=pk)
            
            if author.id == post.author.id:
                post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser])
    def unapproved(self, request):
        try:
            unapprovedPosts = Post.objects.filter(approved=False)
            serializer = PostSerializer(unapprovedPosts, many=True, context={'request': request})
            return Response(serializer.data)   
        
        except Exception as ex:
                return Response({'message': ex.args[0]}) 
            
            
    @action(methods=['put'], detail=True, permission_classes=[IsAdminUser])        
    def approve(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.approved = True
        post.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)   
    
    
    @action(methods=['get'], detail=False)
    def favorites(self, request):
        appuser = AppUser.objects.get(user=request.auth.user)
            
        try:
            likedPosts = Post.objects.filter(liked_by=appuser)
            
            for post in likedPosts:
                post.liked = appuser in post.liked_by.all()
                
            serializer = PostSerializer(likedPosts, many=True, context={'request': request})
            return Response(serializer.data)   
        
        except Exception as ex:
                return Response({'message': ex.args[0]}) 
    
    
    # ?????????????????? Custom Action for the specific url '/like'
    @action(methods=['post', 'delete'], detail=True)
    def like(self, request, pk=None): 
        """Managing appusers liking posts"""
     
        appuser = AppUser.objects.get(user=request.auth.user)

        try:
            # Handle the case if the client specifies a event that doesn't exist
            post = Post.objects.get(pk=pk)
            
        except Post.DoesNotExist:
            return Response(
                {'message': 'Post does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if request.method == "POST":
            try:
                post.liked_by.add(appuser)
                return Response({}, status=status.HTTP_201_CREATED)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined post
        elif request.method == "DELETE":
            try:
                post.liked_by.remove(appuser)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})
            
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializers
    """
    class Meta:
        model = Post
        fields = ('id', 'author', 'publication_date', 'image_url', 'content', 'approved', 'liked')
        depth = 3