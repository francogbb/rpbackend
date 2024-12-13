from rest_framework import serializers
from ...models import ApplicationForm

class ApplicationFormSerializer(serializers.ModelSerializer):
    document_title = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = ApplicationForm
        fields = [
            'id',
            'state',
            'created_at',
            'reason',
            'expiration_date',
            'document',
            'student',
            'document_title',
            'student_name',
        ]
    
    """ Obtiene el título del documento asociado al ApplicationForm """
    def get_document_title(self, obj):
        document = obj.document  
        return document.title if document else None

    """ Obtiene el nombre del profesor guía asociado al PublishForm """
    def get_student_name(self, obj):
        student = obj.student  
        return f'{student.first_name} {student.last_name}' if student else None