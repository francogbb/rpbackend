from rest_framework import viewsets
from ...models import Statistics
from ..serializers.statisticsSerializer import StatisticsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permmission_classes = [AllowAny]
    
    
    @action(detail=False, methods=['get'], url_path='most-viewed')
    def most_viewed(self, request):
        """
        Devuelve los documentos más vistos.
        """
        most_viewed = Statistics.objects.order_by('-views')[:10]
        serializer = StatisticsSerializer(most_viewed, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='most-requested')
    def most_requested(self, request):
        """
        Devuelve los documentos más solicitados.
        """
        most_requested = Statistics.objects.order_by('-requests')[:10]
        serializer = StatisticsSerializer(most_requested, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='all-statistics')
    def list_statistics(self, request):
        """
        Lista todas las estadísticas.
        """
        statistics = Statistics.objects.all()
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Obtiene una estadística específica por ID.
        """
        try:
            statistics = Statistics.objects.get(pk=pk)
            serializer = StatisticsSerializer(statistics)
            return Response(serializer.data)
        except Statistics.DoesNotExist:
            return Response({"error": "Estadística no encontrada."}, status=status.HTTP_404_NOT_FOUND)