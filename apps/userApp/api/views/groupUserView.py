from rest_framework import viewsets
from ...models import GroupUser
from ..serializers.groupUserSerializer import GroupUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class GroupUserViewSet(viewsets.ModelViewSet):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = [IsAuthenticated]
 