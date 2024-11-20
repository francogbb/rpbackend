from rest_framework import serializers
from ...models import Statistics

class StatisticsSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)  # Título del documento

    class Meta:
        model = Statistics
        fields = ['id', 'document', 'document_title', 'views', 'requests', 'last_viewed']
        read_only_fields = ['views', 'requests', 'last_viewed']  # Evitar modificaciones manuales
