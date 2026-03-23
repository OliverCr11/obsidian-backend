from django.urls import path
from .views import GloveList, GloveDetail

urlpatterns = [
    path('products/', GloveList.as_view(), name='product-list'),
    path('products/<slug:slug>/', GloveDetail.as_view(), name='product-detail'),
]
