from rest_framework import serializers
from .models import Glove, Category, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']

class GloveSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Glove
        fields = '__all__'
