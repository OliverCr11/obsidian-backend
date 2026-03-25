from rest_framework import generics
from .models import Glove
from .serializers import GloveSerializer

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
