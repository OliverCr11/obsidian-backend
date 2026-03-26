from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    glove_name = serializers.CharField(source='glove.name', read_only=True)
    glove_name_es = serializers.CharField(source='glove.nameEs', read_only=True, default='')
    glove_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['glove', 'glove_name', 'glove_name_es', 'glove_image', 'price', 'quantity']

    def get_glove_image(self, obj):
        primary = obj.glove.images.filter(is_primary=True).first()
        if primary and primary.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary.image.url)
            return primary.image.url
        first = obj.glove.images.first()
        if first and first.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first.image.url)
            return first.image.url
        return None

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
