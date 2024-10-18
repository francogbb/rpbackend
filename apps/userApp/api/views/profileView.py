from rest_framework import viewsets
from ...models import Profile
from ..serializers.profileSerializer import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
 