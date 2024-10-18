from rest_framework import serializers
from ...models import Document
from apps.userApp.models import Profile

class DocumentSerializer(serializers.ModelSerializer):
    autor = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True)
    class Meta:
        model = Document
        fields = '__all__'