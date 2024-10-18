from rest_framework import viewsets
from ...models import TypeDocument
from ..serializers.typeDocumentSerializer import TypeDocumentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    serializer_class = TypeDocumentSerializer
    permmission_classes = [AllowAny]