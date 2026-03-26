from django.urls import path
from .views import CreateOrderView, UserOrdersView, ApplyCouponView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('my-orders/', UserOrdersView.as_view(), name='my-orders'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
]
