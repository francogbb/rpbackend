from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from ...models import UserAccount, Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

""" Serializer para habilitar el grupo en la creación del usuario desde la interfaz rest_framework """
class UserCreateSerializer(BaseUserCreateSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False) # Obtiene los grupos existentes

    class Meta(BaseUserCreateSerializer.Meta):
        model = UserAccount
        fields = ['email', 'password', 'group']

    def create(self, validated_data):
        
        group = validated_data.pop('group', None)  # Extraer el grupo si es entregado
        user = super().create(validated_data)  # Crea el usuario 
        if group:
            user.group = group  # Asigna el grupo al usuario
            user.save()
        return user

""" Serializer para acceder al atributo name """
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

""" Serializer para que modifica la información obtenida desde la consulta de la url user/me """
class CustomUserSerializer(DjoserUserSerializer):
    group = GroupSerializer(read_only=True)  # Se incluye el grupo al que pertenece el usuario
    profile = serializers.SerializerMethodField()  # Se incluye datos adicionales si es necesario

    class Meta(DjoserUserSerializer.Meta):
        model = UserAccount
        fields = DjoserUserSerializer.Meta.fields + ('group', 'profile')

    def get_profile(self, obj):
        # Verifica si el usuario tiene un perfil y retorna su información
        try:
            profile = Profile.objects.get(user=obj)
            return {
                "id": profile.id,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "section": profile.section.section_name if profile.section else None,
            }
        except Profile.DoesNotExist:
            return None

""" Obtiene todos los usuarios mostrando id, email, password y group{name} """
class UserSerializerProf(serializers.ModelSerializer):
    # Usamos un CharField para recibir el nombre del grupo
    group = serializers.CharField()

    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'password', 'group')
        extra_kwargs = {
            'password': {'write_only': True}  # Para asegurar que la contraseña no se exponga al leer el usuario
        }

    def validate_group(self, value):
        # Valida si el grupo con el nombre proporcionado existe
        try:
            group = Group.objects.get(name=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError("El grupo con este nombre no existe.")
        return group

    def create(self, validated_data):
        # Primero, obtenemos el objeto group a partir del nombre validado
        group = validated_data['group']

        # Creamos el usuario
        user = UserAccount.objects.create(
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Asignamos el grupo al usuario
        user.group = group
        user.set_password(validated_data['password'])  # Encriptamos la contraseña
        user.save()
        return user

class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        """
        Valida la contraseña utilizando las reglas configuradas en Django.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value