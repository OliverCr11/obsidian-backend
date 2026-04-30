from django.urls import path
from .views import CreateOrderView, UserOrdersView, ApplyCouponView, CreatePaymentIntentView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('my-orders/', UserOrdersView.as_view(), name='my-orders'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
]
