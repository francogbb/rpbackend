from rest_framework import viewsets
from ...models import PublishForm
from ..serializers.publishFormSerializer import PublishFormSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class PublishFormViewSet(viewsets.ModelViewSet):
    queryset = PublishForm.objects.all()
    serializer_class = PublishFormSerializer
    permission_classes = [AllowAny]

    """Actualiza solo el estado del PublishForm """
    @action(detail=True, methods=['patch'])
    def update_state(self, request, pk=None):
        publish_instance = self.get_object()
        state = request.data.get('state')
        
        if not state:
            return Response({"error": "El campo 'state' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar solo el campo `state`
        publish_instance.state = state
        publish_instance.save(update_fields=['state'])
        
        return Response({"message": "Estado actualizado correctamente."}, status=status.HTTP_200_OK)
    
    """Actualiza solo el estado del PublishForm basado en el ID del documento asociado """
    @action(detail=False, methods=['patch'], url_path='put-director/(?P<document_id>[^/.]+)')
    def put_director(self, request, document_id=None):

        state = request.data.get('state')  # Nuevo estado

        if not document_id:
            return Response({"error": "El campo 'document_id' es requerido en la URL."}, status=status.HTTP_400_BAD_REQUEST)

        if not state:
            return Response({"error": "El campo 'state' es requerido en el cuerpo."}, status=status.HTTP_400_BAD_REQUEST)

        # Busca el PublishForm relacionado al documento
        try:
            publish_instance = PublishForm.objects.get(document__id=document_id)
        except PublishForm.DoesNotExist:
            return Response({"error": "No se encontró un PublishForm asociado al documento."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar solo el estado
        publish_instance.state = state
        publish_instance.save(update_fields=['state'])

        return Response(
            {
                "message": "Estado actualizado correctamente.",
                "id": publish_instance.id,
                "state": publish_instance.state,
            },
            status=status.HTTP_200_OK
        )
