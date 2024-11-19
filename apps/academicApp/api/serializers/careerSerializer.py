from rest_framework import serializers
from ...models import Career, Area

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'career_name', 'area']



class CareerSerializerView(serializers.ModelSerializer):
    # Definimos un SerializerMethodField para obtener el nombre del área en lugar de su id
    area = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ['id', 'career_name', 'area']

    def get_area(self, obj):
        # Aquí 'obj' es una instancia de Career
        # Obtiene el nombre del área asociada con esta carrera
        return obj.area.area_name
