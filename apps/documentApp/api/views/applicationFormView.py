from rest_framework import viewsets
from ...models import ApplicationForm
from ..serializers.applicationFormSerializer import ApplicationFormSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

class ApplicationFormViewSet(viewsets.ModelViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    permmission_classes = [AllowAny]

    """ Actualiza el estado y se asigna la fecha de expiración """
    @action(detail=True, methods=['patch'])
    def update_state(self, request, pk=None):
        application_instance = self.get_object()
        state = request.data.get('state')
        expiration_date = request.data.get('expiration_date')

        if not state and not expiration_date:
            return Response({"error": "Debe proporcionar 'state' o 'expiration_date' para actualizar."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if state:
            application_instance.state = state
        if expiration_date:
            try:
                application_instance.expiration_date = expiration_date  
            except ValueError:
                return Response({"error": "Formato de fecha inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
        application_instance.save()
        return Response({"message": "Datos actualizados correctamente."}, status=status.HTTP_200_OK)
    
    """ Entrega si existe un ApplicationForm pendiente por documento y estudiante"""
    @action(detail=False, methods=['get'], url_path='filter-application-pending')
    def filter_application_pending(self, request):
        document_id = request.query_params.get('document_id')
        student_id = request.query_params.get('student_id')

        if not document_id or not student_id:
            return Response({"error": "Debe proporcionar 'document_id' y 'student_id'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            application_form = ApplicationForm.objects.get(
                document_id=document_id,
                student_id=student_id,
                state = '1', # Con estado pendiente
            )
        except ApplicationForm.DoesNotExist:
            return Response({"error": "No se encontró un ApplicationForm válido con los parámetros proporcionados."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(application_form)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """ Entrega si existe un ApplicationForm válido por documento y estudiante"""
    @action(detail=False, methods=['get'], url_path='filter-application-student')
    def filter_application_student(self, request):
        document_id = request.query_params.get('document_id')
        student_id = request.query_params.get('student_id')

        if not document_id or not student_id:
            return Response({"error": "Debe proporcionar 'document_id' y 'student_id'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            application_form = ApplicationForm.objects.get(
                document_id=document_id,
                student_id=student_id,
                state='2', # Con estado aprobado
                expiration_date__gt=now()  # Fecha de expiración mayor a la actual
            )
        except ApplicationForm.DoesNotExist:
            return Response({"error": "No se encontró un ApplicationForm válido con los parámetros proporcionados."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(application_form)
        return Response(serializer.data, status=status.HTTP_200_OK)