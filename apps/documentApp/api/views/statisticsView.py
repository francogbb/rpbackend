from rest_framework import viewsets
from ...models import Statistics
from ..serializers.statisticsSerializer import StatisticsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permmission_classes = [AllowAny]