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
    permission_classes = [IsAuthenticated]

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