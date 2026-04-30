from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, Coupon
from .serializers import OrderSerializer
from products.models import Glove
import stripe
import uuid
import threading

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            items = request.data.get('items', [])
            coupon_code = request.data.get('coupon_code')
            
            subtotal = 0
            for item in items:
                try:
                    product = Glove.objects.get(id=item.get('glove'))
                    subtotal += float(product.price) * int(item.get('quantity', 1))
                except Glove.DoesNotExist:
                    pass
            
            discount_amount = 0
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code.upper(), active=True)
                    if coupon.is_valid():
                        if coupon.discount_type == 'fixed':
                            discount_amount = float(coupon.value)
                        else:  # percentage
                            discount_amount = subtotal * (float(coupon.value) / 100)
                except Coupon.DoesNotExist:
                    pass
            
            final_total = max(subtotal - discount_amount, 0)
            if items:
                final_total += 15.00  # SHIPPING RATE

            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(final_total * 100),
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )

            return Response({
                'client_secret': intent.client_secret,
                'calculated_total': final_total
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [AllowAny]

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
                
        user = self.request.user if self.request.user.is_authenticated else None
        
        # Override the status logic, forcing PAID given the Stripe completion dependency
        order = serializer.save(user=user, coupon=coupon, status='PAID')
        
        recipient_email = user.email if user else order.email

        def send_confirmation_email():
            try:
                subject = 'Order Confirmed - Obsidian'
                tracking_id = f"TRK-OBS-{str(order.order_id).split('-')[0].upper()}"
                message = f"Hi {recipient_email}, your order #{order.order_id} for ${order.total_paid} is confirmed. Tracking: {tracking_id}"
                
                html_message = render_to_string('orders/order_confirmation.html', {
                    'order': order,
                    'tracking_id': tracking_id
                })
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email, 'stalincriollo11@gmail.com'], # Admin CC forced to bypass Resend Sandbox restrictions temporarily
                    fail_silently=False,
                    html_message=html_message
                )
            except Exception as e:
                print(f"RESEND SMTP ERROR - Email dispatch failed (Likely Sandbox Domain Restriction or Timeout): {e}")

        # Dispatch email in a background thread to prevent Gunicorn 30s timeout crashes
        email_thread = threading.Thread(target=send_confirmation_email)
        email_thread.start()

class UserOrdersView(generics.ListAPIView):
    """
    Returns a secure temporal list of authenticated Orders filtered exclusively to the requesting JWT User identity.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict user-bound filtering intercepting the resolved JWT identity dynamically
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
