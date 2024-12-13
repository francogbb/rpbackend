from ..serializers.careerSerializer import CareerSerializer
from rest_framework import viewsets
from ...models import Career
from rest_framework.permissions import IsAuthenticated

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [IsAuthenticated]
