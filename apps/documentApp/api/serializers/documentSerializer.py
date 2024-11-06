from rest_framework import serializers
from ...models import Document
from apps.userApp.models import Profile

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
    def validate(self, data):
        # Verifica si el método es POST (creación)
        if self.instance is None and 'document' not in data:
            raise serializers.ValidationError({"document": "El campo 'document' es obligatorio al crear el documento."})
        return data

    def update(self, instance, validated_data):
        # Excluye el campo `document` de los datos validados si está presente
        validated_data.pop('document', None)
        
        # Llama al método `update` del padre con los datos restantes
        return super().update(instance, validated_data)
        
        
