from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from ...models import UserAccount, Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

""" Serializer para habilitar el grupo en la creación del usuario desde la interfaz rest_framework """
class UserCreateSerializer(BaseUserCreateSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        model = UserAccount
        fields = ['email', 'password', 'group']

    def create(self, validated_data):
        group = validated_data.pop('group', None)  # Extraer el grupo si es entregado
        # Crea el usuario directamente sin cifrar la contraseña
        user = UserAccount.objects.create_user(**validated_data)
        if group:
            user.group = group  # Asigna el grupo al usuario
            user.save()
        return user
    
""" Serializer para acceder al atributo name """
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

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
    group = GroupSerializer(read_only=True)
    class Meta:
        model = UserAccount
        fields = ('id','email', 'password', 'group')

class UserSerializerCustomRegister(serializers.ModelSerializer):
    group = serializers.CharField()

    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'password', 'group')
        extra_kwargs = {
            'password': {'write_only': True}  # Para asegurar que la contraseña no se exponga al leer el usuario
        }

    def validate_group(self, value):
        # Valida si el grupo con el nombre proporcionado existe
        print('Valor recibido en validate_group:', value)
        try:
            group = Group.objects.get(name=value)  # Verificamos que el grupo existe
        except Group.DoesNotExist:
            raise serializers.ValidationError("El grupo con este nombre no existe.")
        return group.name  # Devolvemos el nombre del grupo para mantener consistencia

    def create(self, validated_data):
        group_name = validated_data.pop('group')  # Extraemos el nombre del grupo

        try:
            # Verificar si el grupo existe
            group = Group.objects.get(name=group_name)
            print(group)
        except Group.DoesNotExist:
            raise serializers.ValidationError({"group": "El grupo especificado no existe."})

        # Crear el usuario con el grupo asignado
        user = UserAccount.objects.create(
            email=validated_data['email'],
            group=group,  # Asignamos directamente el grupo
        )
        user.set_password(validated_data['password'])  # Encriptar contraseña
        print(user)
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
