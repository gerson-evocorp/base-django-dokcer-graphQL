from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer