from ..serializers.areaSerializer import AreaSerializer
from rest_framework import viewsets
from ...models import Area
from rest_framework.permissions import IsAuthenticated, AllowAny

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]
