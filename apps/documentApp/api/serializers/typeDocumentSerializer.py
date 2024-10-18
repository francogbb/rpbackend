from rest_framework import serializers
from ...models import TypeDocument

class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDocument
        fields = '__all__'