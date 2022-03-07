"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response # 📌 Response will attach the headers, status to the JSON data.
from rest_framework import serializers # 📌 serializers will serialize the data (make it a dictionary), and make it JSON format.
from rest_framework import status
from illuminateapi.models import AppUser, Services

class ServiceView(ViewSet):
    
    def list(self, request):
        """ Handle GET requests to services resource
        Returns:
            Response -- JSON serialized list of services  """
        # Get all game records from the database
        services = Services.objects.all()
        
        # Support filtering services by type： http://localhost:8000/services?type=1
        # That URL will retrieve all tabletop services
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            services = services.filter(gametype__id=game_type)
            # gametype__id has to be a double-underscore.
            # The use of the dunderscore (__) here represents a join operation (foreign-key table).
            # for it's own table, do one underscore

        serializer = ServiceSerializer(
            services, many=True, context={'request': request})
        
        # serializer.data.append(gamer)
        return Response(serializer.data)
    
    

class ServiceSerializer(serializers.ModelSerializer):
    """ JSON serializer for services
    Arguments:
        serializer type  """
    class Meta:
        model = Services
        fields = ('id', 'name', 'location', 'latitude', 'longitude', 'type', 'email', 'phone', 'rating') #the properties in the model
        depth = 2  # relationship depth  <10
        
