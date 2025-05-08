from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer
from .models import Restaurant, Item, RestaurantCart, RestaurantOrder, RestaurantOrderItem




def index(request):
    return render(request, 'base/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('base:index')
        
    if request.method == 'POST':
        login_identifier = request.POST.get('login_identifier')
        password = request.POST.get('password')
        
        if not login_identifier or not password:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'base/login.html')

        # Try to find user by email first
        try:
            user = User.objects.get(email=login_identifier)
            username = user.username
        except User.DoesNotExist:
            # If email doesn't exist, try username
            username = login_identifier

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('base:index')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'base/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('base:index')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not email or not username or not password1 or not password2:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'base/signup.html')
            
        # Check if email is valid
        if not email or '@' not in email or '.' not in email:
            messages.error(request, 'Please enter a valid email address')
            return render(request, 'base/signup.html')
            
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'base/signup.html')
            
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'base/signup.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'base/signup.html')
            
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('base:index')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            
    return render(request, 'base/signup.html')

class SignupAPI(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Signup successful'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['login_identifier']
            password = serializer.validated_data['password']

            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                username = identifier

            user = authenticate(username=username, password=password)

            if user is not None:
                # Set the session
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful',
                    'username': user.username,
                    'email': user.email
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('base:login')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'base/index_pfp.html')

@login_required(login_url='/login/')
def order_history(request):
    return render(request, 'base/order_history.html')

@login_required(login_url='/login/')
def wishlist_view(request):
    return render(request, 'base/wishlist.html')

@login_required(login_url='/login/')
def cart(request):
    return render(request, 'base/cart.html', {
        'user': request.user
    })

@login_required(login_url='/login/')
def vouchers_view(request):
    return render(request, 'base/vouchers.html')

@login_required(login_url='/login/')
def payment(request):
    return render(request, 'base/payment.html', {
        'user': request.user
    })

def TajPalace(request):
    return render(request, 'base/TajPalace.html')

def PunjabGrill(request):
    return render(request, 'base/PunjabGrill.html')

def DosaPlaza(request):
    return render(request, 'base/DosaPlaza.html')

def BiryaniHouse(request):
    return render(request, 'base/BiryaniHouse.html')

def MughalsKitchen(request):
    return render(request, 'base/MughalsKitchen.html')

def SarwanaBhawan(request):
    return render(request, 'base/SarwanaBhawan.html')

# def payment(request):
#     return render(request, 'base/payment.html')

# view changed
from django.shortcuts import render

def order_confirmation(request):
    username = request.user.username  
    return render(request, 'base/order-confirmation.html' , {'username': username})

# Restaurant Views
def restaurant_list(request):
    cuisine_type = request.GET.get('cuisine')
    search_query = request.GET.get('search')
    
    restaurants = Restaurant.objects.filter(is_active=True)
    
    if cuisine_type:
        restaurants = restaurants.filter(cuisine_type=cuisine_type)
    if search_query:
        restaurants = restaurants.filter(name__icontains=search_query)
    
    context = {
        'restaurants': restaurants,
        'cuisine_types': Restaurant._meta.get_field('cuisine_type').choices,
        'current_cuisine': cuisine_type,
        'search_query': search_query,
    }
    return render(request, 'base/restaurant_list.html', context)

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    items = restaurant.items.filter(is_available=True)
    
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    
    context = {
        'restaurant': restaurant,
        'items': items,
        'categories': Item._meta.get_field('category').choices,
        'current_category': category,
    }
    return render(request, 'base/restaurant_detail.html', context)

@login_required
def add_to_restaurant_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            item = Item.objects.get(id=item_id, is_available=True)
            cart_item, created = RestaurantCart.objects.get_or_create(
                user=request.user,
                item=item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
            
            messages.success(request, f'{item.name} added to cart successfully!')
        except Item.DoesNotExist:
            messages.error(request, 'Item not available.')
        except Exception as e:
            messages.error(request, f'Error adding item to cart: {str(e)}')
        
        return redirect('base:restaurant_detail', restaurant_id=item.restaurant.id)
    
    return redirect('base:restaurant_list')

@login_required
def restaurant_cart(request):
    cart_items = RestaurantCart.objects.filter(user=request.user)
    total_amount = sum(item.total for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'base/restaurant_cart.html', context)

@login_required
def remove_from_restaurant_cart(request, item_id):
    try:
        cart_item = RestaurantCart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    except RestaurantCart.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    except Exception as e:
        messages.error(request, f'Error removing item from cart: {str(e)}')
    
    return redirect('base:restaurant_cart')

@login_required
def restaurant_checkout(request):
    cart_items = RestaurantCart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('base:restaurant_list')
    
    try:
        # Get the restaurant from the first item (assuming all items are from the same restaurant)
        restaurant = cart_items.first().item.restaurant
        
        # Create the order
        order = RestaurantOrder.objects.create(
            user=request.user,
            restaurant=restaurant,
            total_amount=sum(item.total for item in cart_items),
            delivery_address=request.user.user_info.address if hasattr(request.user, 'user_info') else ''
        )
        
        # Create order items
        for cart_item in cart_items:
            RestaurantOrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price_at_time=cart_item.item.price
            )
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('base:restaurant_order_history')
    
    except Exception as e:
        messages.error(request, f'Error during checkout: {str(e)}')
        return redirect('base:restaurant_cart')

@login_required
def restaurant_order_history(request):
    orders = RestaurantOrder.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'base/restaurant_order_history.html', context)

def search_restaurants(request):
    query = request.GET.get('q', '')
    if query:
        restaurants = Restaurant.objects.filter(
            is_active=True
        ).filter(
            name__icontains=query
        ) | Restaurant.objects.filter(
            cuisine_type__icontains=query
        )
    else:
        restaurants = Restaurant.objects.none()
    
    return JsonResponse({
        'restaurants': [
            {
                'id': r.id,
                'name': r.name,
                'cuisine_type': r.cuisine_type,
                'rating': float(r.rating),
                'image': r.image
            }
            for r in restaurants[:5]
        ]
    })
