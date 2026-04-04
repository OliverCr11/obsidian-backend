from django.urls import path
from .views import GloveList, GloveDetail, MainDropView

urlpatterns = [
    path('active-hero-drop/', MainDropView.as_view(), name='active-hero-drop'),
    path('products/', GloveList.as_view(), name='product-list'),
    path('products/<int:pk>/', GloveDetail.as_view(), name='product-detail'),
]
