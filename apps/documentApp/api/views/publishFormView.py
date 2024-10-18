from rest_framework import viewsets
from ...models import PublishForm
from ..serializers.publishFormSerializer import PublishFormSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class PublishFormViewSet(viewsets.ModelViewSet):
    queryset = PublishForm.objects.all()
    serializer_class = PublishFormSerializer
    permmission_classes = [AllowAny]