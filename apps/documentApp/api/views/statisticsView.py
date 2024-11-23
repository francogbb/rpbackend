from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDate, TruncYear
from ...models import Statistics
from ..serializers.statisticsSerializer import StatisticsSerializer
from rest_framework.permissions import AllowAny


class StatisticsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar estadísticas de documentos.
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [AllowAny]  # Permitir acceso público

    # -------------------
    # Endpoints Personalizados
    # -------------------

    @action(detail=False, methods=['get'], url_path='most-viewed')
    def most_viewed(self, request):
        """
        Devuelve los 10 documentos más vistos.
        """
        most_viewed = Statistics.objects.order_by('-views')[:5]
        serializer = self.get_serializer(most_viewed, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='most-requested')
    def most_requested(self, request):
        """
        Devuelve los 10 documentos más solicitados.
        """
        most_requested = Statistics.objects.order_by('-requests')[:5]
        serializer = self.get_serializer(most_requested, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-publisher')
    def by_publisher(self, request):
        """
        Devuelve estadísticas agrupadas por publicador.
        """
        statistics = (
            Statistics.objects
            .values('document__publisher')
            .annotate(
                total_views=Sum('views'),
                total_requests=Sum('requests')
            )
            .order_by('-total_views')
        )
        return Response(statistics)

    @action(detail=False, methods=['get'], url_path='by-type-document')
    def by_type_document(self, request):
        """
        Devuelve estadísticas agrupadas por tipo de documento.
        """
        statistics = (
            Statistics.objects
            .values('document__type_document__type_name')
            .annotate(
                total_views=Sum('views'),
                total_requests=Sum('requests')
            )
            .order_by('-total_views')
        )
        return Response(statistics)

    @action(detail=False, methods=['get'], url_path='by-area')
    def by_area(self, request):
        """
        Devuelve estadísticas agrupadas por área.
        """
        statistics = (
            Statistics.objects
            .values('document__area__area_name')  # Cambiar 'name' a 'area_name'
            .annotate(
                total_views=Sum('views'),
                total_requests=Sum('requests'),
                total_documents=Count('document')
            )
            .order_by('-total_views')  # Ordenar por vistas totales
        )
        return Response(statistics)


    @action(detail=False, methods=['get'], url_path='all-statistics')
    def list_statistics(self, request):
        """
        Lista todas las estadísticas.
        """
        statistics = self.get_queryset()
        serializer = self.get_serializer(statistics, many=True)
        return Response(serializer.data)

    # -------------------
    # Métodos Predeterminados
    # -------------------

    def retrieve(self, request, pk=None):
        """
        Devuelve una estadística específica por ID.
        """
        statistics = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(statistics)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-date-uploads')
    def by_date_uploads(self, request):
        """
        Devuelve estadísticas agrupadas por año de subida (entry_date del documento relacionado).
        """
        statistics = (
            Statistics.objects
            .annotate(upload_year=TruncYear('document__entry_date'))  # Agrupar por año
            .values('upload_year')  # Seleccionar solo el año truncado
            .annotate(
                total_uploads=Count('id')  # Contar cuántas estadísticas existen por año
            )
            .order_by('-total_uploads')  # Ordenar por el total de subidas
        )
        
        # Formatear la fecha como 'YYYY'
        for stat in statistics:
            stat['upload_year'] = stat['upload_year'].strftime('%Y')  # Cambiar el formato para solo mostrar 'YYYY'

        return Response(statistics)
    

    @action(detail=False, methods=['get'], url_path='by-access-type-teacher')
    def by_access_type_teacher(self, request):
        """
        Devuelve las estadísticas de documentos vinculados a un profesor,
        agrupados por tipo de acceso (público o privado), usando 'teacher_guide' ID.
        """
        # Obtener el teacher_id desde los parámetros de consulta
        teacher_id = request.query_params.get('teacher_id')
        print(teacher_id)

        if not teacher_id:
            return Response(
                {"error": "Debe proporcionar el 'teacher_id' como parámetro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar por teacher_guide (asegurarse de coincidencia exacta)
        access_type_statistics = (
            Statistics.objects
            .filter(document__teacher_guide=teacher_id)  # Coincidencia exacta
            .values('document__type_access')  # Agrupar por tipo de acceso
            .annotate(
                document = Count('document'),

            )

        )

        # Verificar si hay datos para este teacher_id
        if not access_type_statistics:
            return Response(
                {"error": "No se encontraron estadísticas para el 'teacher_id' proporcionado."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(access_type_statistics, status=status.HTTP_200_OK)
