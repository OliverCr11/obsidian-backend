from rest_framework import generics
from .models import Glove
from .serializers import GloveSerializer

class GloveList(generics.ListAPIView):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Glove.objects.all().order_by('-created_at')
    serializer_class = GloveSerializer

class GloveDetail(generics.RetrieveAPIView):
    """
    API endpoint that retrieves a single product by its unique slug.
    """
    queryset = Glove.objects.all()
    serializer_class = GloveSerializer
    lookup_field = 'slug'
