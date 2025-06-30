from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Order, OrderItem

# ---------------------------
# Session Cart Helper Functions
# ---------------------------
def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

# ---------------------------
# Authentication Views
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------
# Product Views
# ---------------------------
# store/views.py
# store/views.py
def product_list(request, category=None):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/product_list.html', context)



@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# ---------------------------
# Cart Views
# ---------------------------
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart_detail')


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product  # adjust as per your model

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.get_total_price() for item in cart_items)

    return render(request, 'store/cart_detail.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

# ---------------------------
# Order Views
# ---------------------------
@login_required
def place_order(request):
    cart = get_cart(request)
    if not cart:
        return redirect('product_list')

    order = Order.objects.create(user=request.user, completed=True)
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    # Clear cart after placing order
    request.session['cart'] = {}
    return redirect('order_complete')

@login_required
def order_complete(request):
    return render(request, 'store/order_complete.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart_detail')




def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/search_results.html', {'products': products, 'query': query})


from django.shortcuts import redirect

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    order = Order.objects.create(user=request.user, completed=True)
    OrderItem.objects.create(order=order, product=product, quantity=quantity)

    return redirect('order_history')
