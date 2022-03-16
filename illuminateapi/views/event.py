"""View module for handling requests about events"""
from unicodedata import category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from illuminateapi.models import Event, Category, AppUser


class EventView(ViewSet):
    """Illuminate events"""

    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        appuser = AppUser.objects.get(user=request.auth.user)

        # Support filtering events by category
        category = self.request.query_params.get('category', None)
        if category is not None:
            # import pdb; pdb.set_trace()
            events = events.filter(category__label=category) 
        
        # Set the `joined` property on every event
        for event in events:
            event.joined = appuser in event.signed_up_by.all()
           
        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)    
    
    
    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized event instance
        """

        event = Event()
        event.image_url = request.data["image_url"]
        event.name = request.data["name"]
        event.time = request.data["time"]
        event.location = request.data["location"]
        event.host = request.data["host"]
        created_by = AppUser.objects.get(user=request.auth.user)
        event.created_by = created_by
        
        category = Category.objects.get(pk=request.data["category_id"])
        event.category = category

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST) 
        
    
    # ⭕️⭕️⭕️ Custom Action for the specific url '/signup'
    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None): 
        """Managing gamers signing up for events"""
     
        appuser = AppUser.objects.get(user=request.auth.user)

        try:
            # Handle the case if the client specifies a event that doesn't exist
            event = Event.objects.get(pk=pk)
            
        except Event.DoesNotExist:
            return Response(
                {'message': 'Event does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if request.method == "POST":
            try:
                event.signed_up_by.add(appuser)
                return Response({}, status=status.HTTP_201_CREATED)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            try:
                event.signed_up_by.remove(appuser)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})
    
    
    

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    # Serializer with the dependencies goes at the end

    class Meta:
        model = Event # running Event.objects.all()
        fields = ('id', 'image_url', 'name', 'time', 'location', 'host', 'created_by', 'category', 'joined')
