from django.contrib import admin
from .models import Restaurant, Item, RestaurantCart, RestaurantOrder, RestaurantOrderItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'rating', 'is_active', 'phone_number', 'created_at')
    list_filter = ('cuisine_type', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'address', 'phone_number')
    ordering = ('-rating', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_vegetarian', 'is_spicy', 'is_available')
    list_filter = ('restaurant', 'category', 'is_vegetarian', 'is_spicy', 'is_available')
    search_fields = ('name', 'description', 'restaurant__name')
    ordering = ('restaurant', 'category', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RestaurantCart)
class RestaurantCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'subtotal', 'total', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'item__name', 'item__restaurant__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RestaurantOrder)
class RestaurantOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'total_amount', 'status', 'order_datetime')
    list_filter = ('status', 'order_datetime', 'restaurant')
    search_fields = ('user__username', 'restaurant__name', 'delivery_address')
    ordering = ('-order_datetime',)
    readonly_fields = ('order_datetime',)

@admin.register(RestaurantOrderItem)
class RestaurantOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price_at_time', 'subtotal')
    list_filter = ('order__restaurant', 'item__category')
    search_fields = ('order__user__username', 'item__name', 'order__restaurant__name')
    ordering = ('order', 'item')
