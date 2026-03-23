from django.urls import path
from .views import CreateOrderView, OrderListView, ApplyCouponView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('', OrderListView.as_view(), name='order-list'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
]
