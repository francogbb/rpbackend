from rest_framework import serializers
from ...models import Statistics

class StatisticsSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)  
    document_area = serializers.CharField(source='document.area.area_name', read_only=True)  
    document_type = serializers.CharField(source='document.type_document.type_name', read_only=True)  
    document_publisher = serializers.SerializerMethodField()  
    document_academic_degree = serializers.SerializerMethodField()  
    entry_date = serializers.SerializerMethodField()
    type_access = serializers.CharField(source='document.type_access', read_only=True)  
    qualification = serializers.IntegerField(source='document.qualification', read_only=True)  
    avg_qualification = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Statistics
        fields = [
            'id', 'document', 'document_title', 'document_area', 'document_type', 
            'document_publisher', 'document_academic_degree', 'views', 'requests', 'last_viewed', 'entry_date', 'type_access', 'avg_qualification', 'qualification'	]
        
        read_only_fields = ['views', 'requests', 'last_viewed']  # Evitar modificaciones manuales (solo lectura)

    """ Entrega el publicador de un documento """
    def get_document_publisher(self, obj):
        return obj.document.get_publisher_display()  

    """ Entrega el grado académico de un documento """
    def get_document_academic_degree(self, obj):
        return obj.document.get_academic_degree_display()  

    """ Entrega la fecha de creación de un documento """
    def get_entry_date(self, obj):
        if obj.document:
            return obj.document.entry_date
        return None