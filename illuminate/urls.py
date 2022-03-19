"""illuminate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from illuminateapi.views import (
    register_user, 
    login_user, 
    ServiceView, 
    EventView, 
    CategoryView, 
    PostView, 
    AppuserView, 
    get_auth_profile,
    CommentView)


router = routers.DefaultRouter(trailing_slash=False) # not necessary to have "/" in the url
router.register(r'services', ServiceView, 'services')  # part of the controller.  "r" means regex
router.register(r'events', EventView, 'events')
router.register(r'categories', CategoryView, 'categories')
router.register(r'posts', PostView, 'posts') 
router.register(r'comments', CommentView, 'comments') 
router.register(r'appusers', AppuserView, 'appusers')  

# router.register(r'comments', ProfileView, 'profile')


# controller-code
urlpatterns = [
    path('', include(router.urls)),
    
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    
     path('profile', get_auth_profile),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

