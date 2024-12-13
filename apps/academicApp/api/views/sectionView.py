from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ...models import Section
from ....userApp.models import Profile
from ..serializers.sectionSerializer import SectionSerializer, SectionUpdateSerializer
from rest_framework.permissions import IsAuthenticated

""" Obtiene data de relaciones """
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    """ Función que filtra por profesor guía las secciones """
    @action(detail=False, methods=['get'], url_path='by-teacher/(?P<teacher_id>[^/.]+)')
    def by_teacher(self, request, teacher_id=None):
        sections = Section.objects.filter(teacher_guide_id=teacher_id)
        
        if not sections.exists():
            return Response(
                {"message": f"No se encontraron secciones para el teacher_guide con ID {teacher_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = self.get_serializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """ Obtiene los estudiantes asignados a una sección """
    @action(detail=False, methods=['get'], url_path='students-by-section/(?P<section_id>[^/.]+)')
    def students_by_section(self, request, section_id=None):

        students = Profile.objects.filter(section_id=section_id)

        if not students.exists():
            return Response(
                {"message": f"No se encontraron estudiantes para la sección con ID {section_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serializa los datos de los estudiantes
        student_data = [
            {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.user.email,
            }
            for student in students
        ]

        return Response(student_data, status=status.HTTP_200_OK)
    
""" Actualiza la sección """    
class SectionUpdateViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionUpdateSerializer
    permission_classes = [IsAuthenticated]  # Asegura que solo usuarios autenticados puedan acceder

    def get_queryset(self):
        # Opcional: filtra las secciones según permisos o usuarios
        return super().get_queryset()
