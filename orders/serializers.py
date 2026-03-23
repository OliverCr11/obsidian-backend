from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['glove', 'price', 'quantity']

from django.db import transaction

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'full_name', 'email', 'address', 'city', 'total_paid', 'status', 'created_at', 'items']
        read_only_fields = ['order_id', 'status', 'created_at', 'user']
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # User is dynamically injected via the View's perform_create hook
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order
