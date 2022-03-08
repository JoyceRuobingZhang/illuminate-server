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
        
         # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = appuser in event.signed_up_by.all()

        # ⭕️⭕️⭕️ Support filtering events by category
        category = self.request.query_params.get('category', None)
        if category is not None:
            # import pdb; pdb.set_trace()
            events = events.filter(category__label=category) 
           
        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)    
    
    

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    # Serializer with the dependencies goes at the end

    class Meta:
        model = Event # running Event.objects.all()
        fields = ('id', 'image_url', 'name', 'time', 'location', 'host', 'created_by', 'category')
