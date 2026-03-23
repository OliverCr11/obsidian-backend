from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['glove']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'full_name', 'email', 'total_paid', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'full_name', 'email']
    readonly_fields = ['order_id', 'created_at']
    inlines = [OrderItemInline]
