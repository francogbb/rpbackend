from rest_framework import viewsets
from django.contrib.auth.models import User
from ..serializers.userSerializer import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
