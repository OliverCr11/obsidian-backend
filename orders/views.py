from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, Coupon
from .serializers import OrderSerializer

class ApplyCouponView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code', '').upper()
        if not code:
            return Response({'error': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=code)
            if not coupon.is_valid():
                return Response({'error': 'This coupon is expired or inactive.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'value': str(coupon.value)
            }, status=status.HTTP_200_OK)
            
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code.'}, status=status.HTTP_400_BAD_REQUEST)

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        coupon_code = self.request.data.get('coupon_code')
        coupon = None
        if coupon_code:
            try:
                c = Coupon.objects.get(code=coupon_code.upper())
                if c.is_valid():
                    coupon = c
            except Coupon.DoesNotExist:
                pass
                
        order = serializer.save(user=self.request.user, coupon=coupon)
        
        # Native Django SMTP wrapper triggering through Resend Configurations
        try:
            subject = 'Order Confirmed - Obsidian'
            message = f"Hi {self.request.user.email}, your order #{order.order_id} for ${order.total_paid} is confirmed."
            
            # Dynamic Injection extracting structural 'Dark Luxury' elements natively
            html_message = render_to_string('orders/order_confirmation.html', {'order': order})
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.request.user.email],
                fail_silently=False,
                html_message=html_message
            )
        except Exception as e:
            print(f"Email dispatch failed silently: {e}")

class OrderListView(generics.ListAPIView):
    """
    Returns a secure temporal list of authenticated Orders filtered exclusively to the requesting JWT User identity.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict user-bound filtering intercepting the resolved JWT identity dynamically
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
