from ..serializers.signatureSerializer import SignatureSerializer
from rest_framework import viewsets
from ...models import Signature
from rest_framework.permissions import IsAuthenticated

class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated]
