import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Glove

class Coupon(models.Model):
    DISCOUNT_CHOICES = (
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed Amount'),
    )
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, default='PERCENTAGE')
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage (e.g., 20) or Fixed Amount (e.g., 15.00)")
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
    )
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())

    @property
    def discount_amount(self):
        if self.coupon:
            if self.coupon.discount_type == 'PERCENTAGE':
                return self.subtotal * (self.coupon.value / 100)
            return min(self.coupon.value, self.subtotal)
        return 0

    def __str__(self):
        return f"Order {self.order_id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    glove = models.ForeignKey(Glove, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.glove.name} in Order {self.order.order_id}"
