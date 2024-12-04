from rest_framework import viewsets
from ...models import Profile
from ..serializers.profileSerializer import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['patch'])
    def update_section(self, request, pk=None):
        profile_instance = self.get_object()

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

          # Actualizar los campos necesarios
        if first_name:
            profile_instance.first_name = first_name
        if last_name:
            profile_instance.last_name = last_name

        # Guardar solo los campos actualizados
        profile_instance.save(update_fields=['first_name', 'last_name'])

        return Response(
            {
                "message": "Nombre actualizado correctamente.",
                "first_name": profile_instance.first_name,
                "last_name": profile_instance.last_name,
            },
            status=status.HTTP_200_OK
        )
 