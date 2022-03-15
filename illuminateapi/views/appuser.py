"""View module for handling requests about appusers"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from illuminateapi.models import AppUser


class AppuserView(ViewSet):
    """One Appuser"""

    def update(self, request, pk=None):
        """Handle PUT requests for a appuser
        Returns:
            Response -- Empty body with 204 status code
        """
        appuser = AppUser.objects.get(user=request.auth.user)
        
        file = request.data.get('new_file')
        # other_way_to_get_file = request.FILES.get('newFile')
        
        appuser.profile_img = file
        appuser.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)