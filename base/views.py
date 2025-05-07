from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer




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

def wishlist_view(request):
    return render(request, 'base/wishlist.html')
