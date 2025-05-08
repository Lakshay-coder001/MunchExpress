from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')]
    )
    cuisine_type = models.CharField(
        max_length=50,
        choices=[
            ('indian', 'Indian'),
            ('chinese', 'Chinese'),
            ('italian', 'Italian'),
            ('mexican', 'Mexican'),
            ('american', 'American'),
            ('thai', 'Thai'),
            ('japanese', 'Japanese'),
            ('other', 'Other')
        ]
    )
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))],
        default=0.0
    )
    image = models.URLField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.cuisine_type}"

    class Meta:
        ordering = ['-rating', 'name']

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('appetizer', 'Appetizer'),
            ('main_course', 'Main Course'),
            ('dessert', 'Dessert'),
            ('beverage', 'Beverage'),
            ('side_dish', 'Side Dish')
        ]
    )
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    image = models.URLField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    class Meta:
        ordering = ['category', 'name']
        unique_together = ['restaurant', 'name']

class RestaurantCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_carts')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return self.item.price * self.quantity

    @property
    def total_gst(self):
        return self.subtotal * Decimal('0.18')  # 18% GST

    @property
    def total(self):
        return self.subtotal + self.total_gst

    def __str__(self):
        return f"{self.user.username}'s cart - {self.item.name} x {self.quantity}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'item']

class RestaurantOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Item, through='RestaurantOrderItem')
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    delivery_address = models.TextField()
    order_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('preparing', 'Preparing'),
            ('out_for_delivery', 'Out for Delivery'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.restaurant.name}"

    class Meta:
        ordering = ['-order_datetime']

class RestaurantOrderItem(models.Model):
    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price_at_time = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    @property
    def subtotal(self):
        return self.price_at_time * self.quantity

    def __str__(self):
        return f"{self.order.id} - {self.item.name} x {self.quantity}"
