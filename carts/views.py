from django.shortcuts import render, redirect

# Create your views here.

from products.models import Product
from .models import Cart

from orders.models import Order

# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('new cart created')
#     return cart_obj

from accounts.forms import LoginForm

from billing.models import BillingProfile

from accounts.forms import GuestForm

from accounts.models import GuestEmail


def cart_home(request):

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {"cart":cart_obj})


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id', 100) # il 2° arg è il default
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("product is gone?")
            return redirect("cart:home")

        # product_obj = Product.objects.get(id=product_id)
    
        cart_obj, new_obj = Cart.objects.new_or_get(request)
    
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        
        request.session['cart_items'] = cart_obj.products.count()

    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")    

    user = request.user
    billing_profile = None

    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)

    else:
        pass

        order_qs = Order.objects.filter(cart=cart_obj, active=True)
        
        if order_qs.exists():
            order_qs.update(active=False)
        else:
            order_obj = Order.objects.create(
                billing_profile=billing_profile, 
                cart=cart_obj)
        


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form" : guest_form

    }

    return render(request, "carts/checkout.html", context )