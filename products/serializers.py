from rest_framework import serializers
from .models import Glove, Category, ProductImage

class GloveSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Glove
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        if not request:
            return [img.image.url for img in obj.images.all()]
        return [request.build_absolute_uri(img.image.url) for img in obj.images.all()]
