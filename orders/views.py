from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # Explicitly enforce user integrity mapping cleanly to authentication header properties
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderListView(generics.ListAPIView):
    """
    Returns a secure temporal list of authenticated Orders filtered exclusively to the requesting JWT User identity.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict user-bound filtering intercepting the resolved JWT identity dynamically
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
