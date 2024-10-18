from rest_framework import viewsets
from ...models import ApplicationForm
from ..serializers.applicationFormSerializer import ApplicationFormSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ApplicationFormViewSet(viewsets.ModelViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    permmission_classes = [AllowAny]