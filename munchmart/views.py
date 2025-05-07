from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from .models import GroceryItem, Cart, OrderHistory

# Create your views here.


def index_grocery(request):
    featured_items = GroceryItem.objects.filter(stock__gt=0)[:6]
    context = {
        'featured_items': featured_items,
    }
    return render(request, 'munchmart/index_grocery.html', context)

def products(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    
    items = GroceryItem.objects.filter(stock__gt=0)
    
    if category:
        items = items.filter(type=category)
    if search_query:
        items = items.filter(name__icontains=search_query)
    
    context = {
        'items': items,
        'categories': GroceryItem._meta.get_field('type').choices,
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'munchmart/products.html', context)

@login_required
def cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            grocery_item = GroceryItem.objects.get(id=item_id, stock__gte=quantity)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                grocery_item=grocery_item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
            
            messages.success(request, f'{grocery_item.name} added to cart successfully!')
        except GroceryItem.DoesNotExist:
            messages.error(request, 'Item not available in requested quantity.')
        except Exception as e:
            messages.error(request, f'Error adding item to cart: {str(e)}')
        
        return redirect('munchmart:cart')
    
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'munchmart/cart_munch.html', context)

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    except Cart.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    except Exception as e:
        messages.error(request, f'Error removing item from cart: {str(e)}')
    
    return redirect('munchmart:cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('munchmart:products')
    
    try:
        for cart_item in cart_items:
            if cart_item.grocery_item.stock < cart_item.quantity:
                messages.error(request, f'Insufficient stock for {cart_item.grocery_item.name}')
                return redirect('munchmart:cart')
            
            OrderHistory.objects.create(
                user=request.user,
                grocery_item=cart_item.grocery_item,
                quantity=cart_item.quantity,
                total_payment=cart_item.total
            )
            
            # Update stock
            cart_item.grocery_item.stock -= cart_item.quantity
            cart_item.grocery_item.save()
        
        # Clear cart after successful checkout
        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('munchmart:order_history')
    
    except Exception as e:
        messages.error(request, f'Error during checkout: {str(e)}')
        return redirect('munchmart:cart')

@login_required
def order_history(request):
    orders = OrderHistory.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'munchmart/order_history.html', context)