from ..serializers.userSerializers import UserCreateSerializer, UserSerializerProf, PasswordUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import UserAccount
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.password_validation import validate_password


class CustomUserView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [ AllowAny ]
    
    
class CustomUserProfView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializerProf
    permission_classes = [ AllowAny ]


    @action(detail=True, methods=['patch'])
    def update_password(self, request, pk=None):
        """
        Endpoint para actualizar exclusivamente la contraseña.
        """
        user_instance = self.get_object()
        serializer = PasswordUpdateSerializer(data=request.data)

        # Validar los datos
        serializer.is_valid(raise_exception=True)

        # Actualizar la contraseña
        password = serializer.validated_data['password']
        user_instance.set_password(password)
        user_instance.save()

        return Response(
            {"message": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK
        )