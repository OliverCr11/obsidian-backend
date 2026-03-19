from django.urls import path
from .views import GloveList

urlpatterns = [
    path('products/', GloveList.as_view(), name='product-list'),
]
