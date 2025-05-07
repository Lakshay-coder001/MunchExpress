from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')]
    )
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s contact info"

    class Meta:
        ordering = ['-created_at']

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    review = models.CharField(max_length=50)
    image = models.URLField(max_length=200)
    type = models.CharField(
        max_length=50,
        choices=[
            ('vegetable', 'Vegetable'),
            ('fruit', 'Fruit'),
            ('dairy', 'Dairy'),
            ('grain', 'Grain'),
            ('snack', 'Snack'),
            ('beverage', 'Beverage'),
        ]
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.quantity} @ ₹{self.price}"

    class Meta:
        ordering = ['name']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    grocery_item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return self.grocery_item.price * self.quantity

    @property
    def total_gst(self):
        return self.subtotal * Decimal('0.18')  # 18% GST

    @property
    def total(self):
        return self.subtotal + self.total_gst

    def __str__(self):
        return f"{self.user.username}'s cart - {self.grocery_item.name} x {self.quantity}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'grocery_item']

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    grocery_item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE, related_name='order_history')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    total_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    order_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.grocery_item.name}"

    class Meta:
        ordering = ['-order_datetime']
        verbose_name_plural = 'Order History'