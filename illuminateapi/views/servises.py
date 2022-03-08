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
        service_type = self.request.query_params.get('type', None)
        # import pdb; pdb.set_trace()
        is_online = self.request.query_params.get('isOnline', None)
        is_sliding_scale = self.request.query_params.get('isOnline', None)

        if service_type:
            services = services.filter(type=service_type)
        
        if is_online == "true":
            services = services.filter(online=True)
            
        if is_sliding_scale == "true":
            services = services.filter(sliding_scale=True)
       
    

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
        fields = ('id', 'name', 'location', 'latitude', 'longitude', 'type', 
                  'email', 'phone', 'rating', 'sliding_scale', 'online') #the properties in the model
        depth = 2  # relationship depth  <10
        
