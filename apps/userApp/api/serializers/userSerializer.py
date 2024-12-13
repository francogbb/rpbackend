from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password') # Solo se utiliza email y password del modelo User

    """ Se modifica el serializar para la creación de un usuario """
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email']  # Usamos el email como username
        )
        user.set_password(validated_data['password'])  # Encriptar la contraseña
        user.save()
        return user

    """ Valida si un email existe """
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Este email ya está en uso.")
        return value