from rest_framework import serializers
from ...models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
        

class AreaSerializerModField(serializers.ModelSerializer):
    # Campo personalizado para mostrar el email del director
    director_email = serializers.EmailField(source='director.email', read_only=True)
    class Meta:
        model = Area
        fields = ['id', 'area_name', 'director_email']  # Lista los campos que quieres incluir