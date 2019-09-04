from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from .api.viewsets import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('api-token-auth/', obtain_jwt_token),
     path('refresh-token/', refresh_jwt_token),
]

