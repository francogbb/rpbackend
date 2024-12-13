from ..serializers.userSerializers import UserCreateSerializer, UserSerializerProf, UserSerializerCustomRegister, PasswordUpdateSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticated
from ...models import UserAccount
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class CustomUserView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [ IsAuthenticated ]
    
    
class CustomUserProfView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializerProf
    permission_classes = [ IsAuthenticated ]


class CustomUserRegisterEditView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializerCustomRegister
    permission_classes = [ IsAuthenticated ]
    
    
class PasswordUpdateView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    """ Función que permite la actualización de la contraseña """
    @action(detail=False, methods=["put"], url_path="change-password")
    def change_password(self, request):
        print("Request data:", request.data)  # Depura los datos recibidos
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        print("Serializer errors:", serializer.errors)  # Imprime los errores del serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
