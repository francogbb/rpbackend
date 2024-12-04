from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ...models import Section
from ..serializers.sectionSerializer import SectionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    """ Función que filtra por profesor guía las secciones """
    @action(detail=False, methods=['get'], url_path='by-teacher/(?P<teacher_id>[^/.]+)')
    def by_teacher(self, request, teacher_id=None):
        """
        Acción personalizada para obtener secciones filtradas por teacher_guide.
        """
        sections = Section.objects.filter(teacher_guide_id=teacher_id)
        
        if not sections.exists():
            return Response(
                {"message": f"No se encontraron secciones para el teacher_guide con ID {teacher_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = self.get_serializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

