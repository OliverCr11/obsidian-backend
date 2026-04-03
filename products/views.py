from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Glove
from .serializers import GloveSerializer

class MainDropView(APIView):
    """
    API endpoint that returns the SINGLE active featured drop for the Hero section.
    """
    def get(self, request):
        featured_glove = Glove.objects.filter(is_hero_drop=True).order_by('-created_at').first()
        if not featured_glove:
            return Response({"detail": "No hero drop found"}, status=404)
        
        # Get primary image
        primary_image = featured_glove.images.filter(is_primary=True).first()
        backup_image = featured_glove.images.first()
        image_url = ""
        
        if primary_image and primary_image.image:
            image_url = primary_image.image.url 
        elif backup_image and backup_image.image:
            image_url = backup_image.image.url

        return Response({
            "id": featured_glove.id,
            "name": featured_glove.name,
            "description": featured_glove.description,
            "price": str(featured_glove.price),
            "hero_title_over_the_product": featured_glove.hero_title_over_the_product,
            "hero_marketing_description": featured_glove.hero_marketing_description,
            "limited_drop_info_text": featured_glove.limited_drop_info_text,
            "countdown_target_date": featured_glove.countdown_target_date.isoformat() if featured_glove.countdown_target_date else None,
            "image_url": image_url
        })

class GloveList(generics.ListAPIView):
    """
    API endpoint that allows products to be viewed.
    """
    serializer_class = GloveSerializer

    def get_queryset(self):
        queryset = Glove.objects.all().order_by('-created_at')
        collection = self.request.query_params.get('collection_type', None)
        if collection:
            queryset = queryset.filter(collection_type=collection.upper())
        return queryset

class GloveDetail(generics.RetrieveAPIView):
    """
    API endpoint that retrieves a single product by its unique slug.
    """
    queryset = Glove.objects.all()
    serializer_class = GloveSerializer
    lookup_field = 'slug'
