from ..serializers.sectionSerializer import SectionSerializer
from rest_framework import viewsets
from ...models import Section
from rest_framework.permissions import IsAuthenticated, AllowAny

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]
