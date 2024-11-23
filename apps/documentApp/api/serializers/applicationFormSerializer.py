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
    
    def get_document_title(self, obj):
        # Obtiene el título del documento asociado al ApplicationForm
        document = obj.document  # Obtiene el objeto Document del documento del ApplicationForm
        return document.title if document else None

    def get_student_name(self, obj):
        # Obtiene el nombre del profesor guía asociado al PublishForm
        student = obj.student  # Obtiene el objeto Profile del Estudiante
        return f'{student.first_name} {student.last_name}' if student else None