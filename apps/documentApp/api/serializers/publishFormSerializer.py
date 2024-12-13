from rest_framework import serializers
from ...models import PublishForm

class PublishFormSerializer(serializers.ModelSerializer):
    document_title = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    area_name = serializers.SerializerMethodField()

    class Meta:
        model = PublishForm
        fields = [
            'id',
            'state',
            'document',
            'created_at',
            'teacher_guide',
            'document_title',
            'teacher_name',
            'area',
            'area_name'
        ]

    """ Obtiene el título del documento asociado al PublishForm """
    def get_document_title(self, obj):
        document = obj.document  
        return document.title if document else None

    """ Obtiene el nombre del profesor guía asociado al PublishForm """
    def get_teacher_name(self, obj):
        teacher_guide = obj.teacher_guide  
        return f'{teacher_guide.first_name} {teacher_guide.last_name}' if teacher_guide else None
    
    """ Obtiene el área asociada al documento del PublishForm """
    def get_area(self, obj):
        document = obj.document  
        area = document.area if document else None  
        return area.id 
    
    """ Obtiene el nombre del área asociada al documento del PublishForm """
    def get_area_name(self, obj):
        document = obj.document  
        area = document.area if document else None  
        return area.area_name  


class PublishFormAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishForm
        fields = ['document']