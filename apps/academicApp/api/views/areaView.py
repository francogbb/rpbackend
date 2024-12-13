from ..serializers.areaSerializer import AreaSerializer, AreaSerializerModField
from rest_framework import status, viewsets
from ...models import Area
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

""" Actualiza solo algunos campos de Área (PATCH)"""
class AreaModViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializerModField
    permission_classes = [IsAuthenticated]

    """ Permite actualizar los campos "area_name" y "director" de un área """
    @action(detail=True, methods=['patch'], url_path='update-director')
    def update_director(self, request, pk=None):

        try:
            area = self.get_object()
        except Area.DoesNotExist:
            return Response(
                {"error": "El área especificada no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        area_name = request.data.get('area_name')
        director = request.data.get('director')

        # Validar que al menos uno de los campos esté presente
        if area_name is None and director is None:
            return Response(
                {"error": "Debe proporcionar al menos el campo 'area_name' o 'director'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualiza los campos proporcionados
        if area_name is not None:
            area.area_name = area_name
        if director is not None:
            area.director_id = director  # Asignar el ID del director

        # Guarda los cambios
        area.save()

        # Serializa y devuelve la respuesta
        serializer = self.get_serializer(area)
        return Response(serializer.data, status=status.HTTP_200_OK)