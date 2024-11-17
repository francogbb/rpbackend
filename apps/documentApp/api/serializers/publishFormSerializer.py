from rest_framework import serializers
from ...models import PublishForm

class PublishFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishForm
        fields = '__all__'

class PublishFormAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishForm
        fields = ['document']