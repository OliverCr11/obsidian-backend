from rest_framework import serializers
from .models import Glove

class GloveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glove
        fields = '__all__'
