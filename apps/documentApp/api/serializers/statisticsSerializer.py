from rest_framework import serializers
from ...models import Statistics

class StatisticsSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)  # Título del documento
    document_area = serializers.CharField(source='document.area.area_name', read_only=True)  # Nombre del área
    document_type = serializers.CharField(source='document.type_document.type_name', read_only=True)  # Tipo de documento
    document_publisher = serializers.SerializerMethodField()  # Publicador legible
    document_academic_degree = serializers.SerializerMethodField()  # Grado académico legible
    entry_date = serializers.SerializerMethodField()
    type_access = serializers.CharField(source='document.type_access', read_only=True)  # Tipo de acceso

    
    class Meta:
        model = Statistics
        fields = [
            'id', 'document', 'document_title', 'document_area', 'document_type', 
            'document_publisher', 'document_academic_degree', 'views', 'requests', 'last_viewed', 'entry_date', 'type_access']
        
        read_only_fields = ['views', 'requests', 'last_viewed']  # Evitar modificaciones manuales

    def get_document_publisher(self, obj):
        return obj.document.get_publisher_display()  # Obtener etiqueta legible de publisher

    def get_document_academic_degree(self, obj):
        return obj.document.get_academic_degree_display()  # Obtener etiqueta legible de academic_degree

    def get_entry_date(self, obj):
        # Accede al campo entry_date desde el documento relacionado
        if obj.document:
            return obj.document.entry_date
        return None