from django.shortcuts import render

from django.shortcuts import render

def index(request):
    return render(request, 'munchmart/index_grocery.html')  # or 'New_grocery.html'

def index_grocery(request):  # Add this view
    return render(request, 'munchmart/index_grocery.html')

def cart(request):
    return render(request, 'munchmart/cart.html')

from django.shortcuts import render

def wishlist(request):
    return render(request, 'munchmart/wishlist.html')  # For Option A
    # or return render(request, 'wishlist.html')  # For Option B