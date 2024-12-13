from rest_framework import viewsets
from ...models import Profile
from ..serializers.profileSerializer import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ....academicApp.models import Section
from rest_framework.exceptions import ValidationError

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    """ Actualiza el perfil (Sirve para la creación de un usuario y modificar el profilo creado con el signal) """
    @action(detail=True, methods=['patch'])
    def update_section(self, request, pk=None):
        profile_instance = self.get_object()

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        section = request.data.get('section')

        # Validar y actualizar los campos necesarios
        if first_name:
            profile_instance.first_name = first_name
        if last_name:
            profile_instance.last_name = last_name
        if section:
            if section == "null" or section is None or section == "":
                profile_instance.section = None
            else:
                try:
                    profile_instance.section = Section.objects.get(id=int(section))
                except (ValueError, Section.DoesNotExist):
                    raise ValidationError({"section": "El valor proporcionado para la sección no es válido."})

        # Guardar solo los campos actualizados
        profile_instance.save(update_fields=['first_name', 'last_name', 'section'])

        return Response(
            {
                "message": "Perfil actualizado correctamente.",
                "first_name": profile_instance.first_name,
                "last_name": profile_instance.last_name,
                "section": profile_instance.section.id if profile_instance.section else None,
            },
            status=status.HTTP_200_OK
        )