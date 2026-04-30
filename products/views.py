from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Glove
from .serializers import GloveSerializer

from rest_framework.permissions import AllowAny

class MainDropView(APIView):
    permission_classes = [AllowAny]
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

        serializer_data = GloveSerializer(featured_glove).data
        serializer_data["image_url"] = image_url

        return Response(serializer_data)

class GloveList(generics.ListAPIView):
    """
    API endpoint that allows products to be viewed.
    """
    serializer_class = GloveSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Glove.objects.all().order_by('-created_at')
        collection = self.request.query_params.get('collection_type', None)
        if collection:
            queryset = queryset.filter(collection_type=collection.upper())
        return queryset

class GloveDetail(generics.RetrieveAPIView):
    """
    API endpoint that retrieves a single product by its unique ID.
    """
    queryset = Glove.objects.all()
    serializer_class = GloveSerializer
    permission_classes = [AllowAny]
