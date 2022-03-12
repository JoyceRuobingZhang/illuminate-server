from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers

from illuminateapi.models import AppUser
from illuminateapi.views.event import EventSerializer


@api_view(['GET'])
def get_auth_profile(request):
    appuser = request.auth.user.appuser

    serializer = AppUserSerializer(appuser, context={'request': request})

    return Response(serializer.data)


class AppUserSerializer(serializers.ModelSerializer):

    signed_up_events = EventSerializer(many=True)

    class Meta:
        model = AppUser
        fields = ('id', 'bio', 'profile_img', 'signed_up_events')