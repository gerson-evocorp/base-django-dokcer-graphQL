from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from .api.viewsets import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('api-token-auth/', views.obtain_auth_token)
]

