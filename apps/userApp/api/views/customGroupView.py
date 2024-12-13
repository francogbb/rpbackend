from rest_framework import viewsets
from ...models import CustomGroup
from ..serializers.customGroupSerializer import CustomGroupSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class CustomGroupViewSet(viewsets.ModelViewSet):
    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer
    permission_classes = [IsAuthenticated]
 