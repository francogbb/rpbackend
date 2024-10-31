from rest_framework import serializers
from ...models import Document
from apps.userApp.models import Profile

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'