from rest_framework import serializers
from .models import Glove, Category

class GloveSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    class Meta:
        model = Glove
        fields = '__all__'
