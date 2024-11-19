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
                "area": profile.area.area_name if profile.area else None,
            }
        except Profile.DoesNotExist:
            return None


class UserSerializerProf(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id','email', 'password', 'group')

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