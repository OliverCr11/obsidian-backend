from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # Explicitly enforce user integrity mapping cleanly to authentication header properties
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        
        # Native Django SMTP wrapper triggering through Resend Configurations
        try:
            subject = 'Order Confirmed - Obsidian'
            message = f"Hi {self.request.user.email}, your order #{order.order_id} for ${order.total_paid} is confirmed."
            html_message = f"Hi <strong>{self.request.user.email}</strong>, your order #{str(order.order_id).split('-')[0].upper()} for <strong>${order.total_paid}</strong> is confirmed. Welcome to Obsidian Core."
            
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
