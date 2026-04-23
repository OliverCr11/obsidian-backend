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
        fields = (
            'id',
            'category',
            'collection_type',
            'name',
            'name_es',
            'name_en',
            'slug',
            'description',
            'description_es',
            'description_en',
            'price',
            'stock',
            'size',
            'is_hero_drop',
            'hero_title_over_the_product',
            'hero_title_over_the_product_es',
            'hero_title_over_the_product_en',
            'hero_marketing_description',
            'hero_marketing_description_es',
            'hero_marketing_description_en',
            'limited_drop_info_text',
            'countdown_target_date',
            'created_at',
            'images',
        )
