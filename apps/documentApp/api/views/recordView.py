from rest_framework import viewsets
from ...models import Record
from ..serializers.recordSerializer import RecordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permmission_classes = [AllowAny]