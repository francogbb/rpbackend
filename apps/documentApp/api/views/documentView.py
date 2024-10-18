from rest_framework import viewsets
from ...models import Document
from ..serializers.documentSerializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permmission_classes = [AllowAny]