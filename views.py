from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator


# PRODUCT VIEW
class ProductView(View):
    def get(self, request):
        # Fetching all product categories in a single query
        categories = ['M', 'L', 'MT', 'MB', 'WT', 'WB', 'B', 'G', 'TW', 'BW']
        products = {category: Product.objects.filter(category=category) for category in categories}

        return render(request, 'app/home.html', products)


# PRODUCT DETAILS VIEW
class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)  # Improved error handling with get_object_or_404
        item_already_in_cart = False
        
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


# ADD TO CART VIEW
@login_required
def add_to_cart(request):
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)  # Improved error handling
    Cart.objects.get_or_create(user=request.user, product=product)  # Avoid duplicates
    return redirect('/cart')


# SHOW CART VIEW
@login_required
def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    if cart_items.exists():
        total_amount, shipping_amount = calculate_cart_totals(cart_items)
        return render(request, 'app/addtocart.html', {'carts': cart_items, 'amount': total_amount - shipping_amount, 'total_amount': total_amount})
    else:
        return render(request, 'app/emptycart.html')


# Function to calculate total amounts
def calculate_cart_totals(cart_items):
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping_amount = 50.0
    total_amount = amount + shipping_amount
    return total_amount, shipping_amount


# Plus Button View
@login_required
def plus_cart(request):
    return update_cart_quantity(request, 1)


# Minus Button View
@login_required
def minus_cart(request):
    return update_cart_quantity(request, -1)


# Common function to update cart quantity
def update_cart_quantity(request, change):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, Q(product=prod_id) & Q(user=request.user))
        
        cart_item.quantity += change
        
        if cart_item.quantity <= 0:
            cart_item.delete()  # Remove the item if quantity is zero
        else:
            cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount, shipping_amount = calculate_cart_totals(cart_items)
        
        data = {
            'quantity': cart_item.quantity,
            'amount': total_amount - shipping_amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)


# REMOVE CART BUTTON VIEW
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, Q(product=prod_id) & Q(user=request.user))
        cart_item.delete()  # Safely delete the cart item

        cart_items = Cart.objects.filter(user=request.user)
        total_amount, shipping_amount = calculate_cart_totals(cart_items)
        
        data = {
            'amount': total_amount - shipping_amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)


# LOGIN VIEW
@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


# ORDER VIEW
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


# PRODUCT VIEW
def product_view(request, category, data=None):
    # Filter products based on category and data
    if data is None:
        products = Product.objects.filter(category=category)
    elif data in ['Below', 'Above']:
        price_condition = (Product.discounted_price < 10000) if data == 'Below' else (Product.discounted_price > 10000)
        products = Product.objects.filter(category=category).filter(price_condition)
    else:
        products = Product.objects.filter(category=category).filter(brand=data)

    template_map = {
        'M': 'app/mobile.html',
        'L': 'app/laptop.html',
        'MT': 'app/mentopwear.html',
        'MB': 'app/menbottomwear.html',
        'WT': 'app/womentopwear.html',
        'WB': 'app/womenbottomwear.html',
        'B': 'app/boyswear.html',
        'G': 'app/girlswear.html'
    }

    return render(request, template_map[category], {f'{category}': products})


# Mobile View
def mobile(request, data=None):
    return product_view(request, 'M', data)


# Laptop View
def laptop(request, data=None):
    return product_view(request, 'L', data)


# Men Top Wear View
def mentopwear(request, data=None):
    return product_view(request, 'MT', data)


# Men Bottom Wear View
def menbottomwear(request, data=None):
    return product_view(request, 'MB', data)


# Women Top Wear View
def womentopwear(request, data=None):
    return product_view(request, 'WT', data)


# Women Bottom Wear View
def womenbottomwear(request, data=None):
    return product_view(request, 'WB', data)


# Boys Wear View
def boyswear(request, data=None):
    return product_view(request, 'B', data)


# Girls Wear View
def girlswear(request, data=None):
    return product_view(request, 'G', data)




# CHECKOUT VIEW
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart_items)
    shipping_amount = 50.0
    total_amount = amount + shipping_amount if cart_items else 0.0

    return render(request, 'app/checkout.html', {
        'add': add,
        'total_amount': total_amount,
        'amount': amount,
        'cart_items': cart_items
    })


# PAYMENT DONE VIEW
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = get_object_or_404(Customer, id=custid)
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity
        )
        c.delete()
    
    return redirect("orders")


# CUSTOMER REGISTRATION VIEW
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations..! Registered Successfully.')
            return redirect('login')  # Redirect to login or another appropriate page
        return render(request, 'app/customerregistration.html', {'form': form})


# PROFILE VIEW
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer_data = {
                'user': request.user,
                'name': form.cleaned_data['name'],
                'locality': form.cleaned_data['locality'],
                'city': form.cleaned_data['city'],
                'state': form.cleaned_data['state'],
                'zipcode': form.cleaned_data['zipcode']
            }
            Customer.objects.update_or_create(user=request.user, defaults=customer_data)
            messages.success(request, 'Congratulations! Profile Updated Successfully')

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


# ADDRESS VIEW
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

