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

    def get_document_title(self, obj):
        # Obtiene el título del documento asociado al PublishForm
        document = obj.document  # Obtiene el objeto Document del documento del publishform
        return document.title if document else None

    def get_teacher_name(self, obj):
        # Obtiene el nombre del profesor guía asociado al PublishForm
        teacher_guide = obj.teacher_guide  # Obtiene el objeto Profile del Teacher Guide
        return f'{teacher_guide.first_name} {teacher_guide.last_name}' if teacher_guide else None
    def get_area(self, obj):
        # Obtiene el área asociada al documento del PublishForm
        document = obj.document  # Obtiene el objeto Document relacionado con el PublishForm
        area = document.area if document else None  # Accede al área del documento
        return area.id 
    def get_area_name(self, obj):
        # Obtiene el área asociada al documento del PublishForm
        document = obj.document  # Obtiene el objeto Document relacionado con el PublishForm
        area = document.area if document else None  # Accede al área del documento
        return area.area_name  # Asumiendo que el área tiene un campo `name`


class PublishFormAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishForm
        fields = ['document']