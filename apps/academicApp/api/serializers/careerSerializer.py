from rest_framework import serializers
from ...models import Career, Area

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'career_name', 'area']

class CareerSerializerView(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ['id', 'career_name', 'area']

    """ Obtiene el nombre del área perteneciente """
    def get_area(self, obj):
        return obj.area.area_name
