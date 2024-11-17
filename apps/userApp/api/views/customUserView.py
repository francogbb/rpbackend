from ..serializers.userSerializers import UserCreateSerializer, UserSerializerProf
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import UserAccount
from rest_framework import viewsets


class CustomUserView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [ AllowAny ]
    
    
class CustomUserProfView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializerProf
    permission_classes = [ AllowAny ]