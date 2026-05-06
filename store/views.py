from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def home(request):
    products = Product.objects.filter(available=True)[:8]
    return render(request, 'store/home.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return render(request, 'store/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    profile_updated = False
    profile_error = ''
    if request.method == 'POST':
        username = request.POST.get('username', request.user.username).strip()
        email = request.POST.get('email', request.user.email).strip()
        first_name = request.POST.get('first_name', request.user.first_name).strip()
        last_name = request.POST.get('last_name', request.user.last_name).strip()
        if username != request.user.username and User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            profile_error = 'That username is already taken.'
        elif email and email != request.user.email and User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            profile_error = 'That email is already used by another account.'
        else:
            request.user.username = username
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            profile_updated = True
    return render(request, 'store/profile.html', {
        'orders': orders,
        'profile_updated': profile_updated,
        'profile_error': profile_error,
    })

def products(request):
    products = Product.objects.filter(available=True)
    return render(request, 'store/products.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        count = sum(cart.values())
        return JsonResponse({'success': True, 'message': f'{product.name} added to cart!', 'cart_count': count})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})

@login_required
def buy_now(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = {str(product_id): 1}
        request.session['cart'] = cart
        return redirect('checkout')
    except Product.DoesNotExist:
        return redirect('products')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        elif str(product_id) in cart:
            del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = float(product.price) * quantity
            total += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue
    return render(request, 'store/cart.html', {'items': items, 'total': total, 'cart_count': len(items)})

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('products')
    
    items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = float(product.price) * quantity
            total += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue
    
    if request.method == 'POST':
        if not items:
            return redirect('cart')
        order = Order.objects.create(user=request.user, total=0)
        order_total = 0
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            order_total += item['subtotal']
        order.total = order_total
        order.save()
        request.session['cart'] = {}
        return redirect('checkout_success')
    
    return render(request, 'store/checkout.html', {'items': items, 'total': total})

@login_required
def checkout_success(request):
    return render(request, 'store/checkout_success.html')
