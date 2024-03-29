from django.shortcuts import render, redirect

# Create your views here.

from products.models import Product
from .models import Cart

from orders.models import Order

from accounts.forms import LoginForm

from billing.models import BillingProfile

from accounts.forms import GuestForm

from accounts.models import GuestEmail

from addresses.forms import AddressForm

from addresses.models import Address

from django.http import JsonResponse


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()  # list of objects

    # se ritorno un dizionario dalla vista, django permette di richiamare i suoi elementi con il django tag nei template
    # se ritorno una json response, devo cambiare il modo in cui il dato è richiamato nel template

    # this is data serialization: data are transformed in a format which is recognizable by the response
    products = [
        {
            "id":       x.id,
            "url":      x.get_absolute_url(),
            "name":     x.name,
            "price":    x.price,            
        }
        for x in cart_obj.products.all()
    ]

    # dict_for_jsonresponse
    cart_data = {
            "products": products,
            "subtotal": cart_obj.subtotal,
            "total": cart_obj.total

        }

    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart":cart_obj} )


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
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        
        request.session['cart_items'] = cart_obj.products.count()

    if request.is_ajax(): # asinchronous javascript and xml
        print("Ajax request")
        # se la richiesta è ajax, devo ritornare dati usando il formato ajax -> jsonresponse
        # quindi lo aggiungo usando jsonresoonse
        dict_for_jsonresponse = {
            "added": added,
            "removed": not added, # sto aggiungendo l'opposto,
            "cartItemCount": cart_obj.products.count()  # camelcase perche diventa la key di un json
        }
        
        json_response = JsonResponse(dict_for_jsonresponse)

        # return JsonResponse({"message": "OHNOOO error 400"}, status=400)  # PROVA ERRORE
        return json_response  # ok

    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")    

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)


    billing_profile = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        print("billing_profile exists")

        if request.user.is_authenticated:
        
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            # shipping_address_qs = address_qs.filter(address_type="shipping")
            # billing_address_qs = address_qs.filter(address_type="billing")

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        
        if shipping_address_id:
            print("shipping_address exists")
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]

        if billing_address_id:
            print("billing_address exists")
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]

        if billing_address_id or shipping_address_id:
            order_obj.save()
            print("order_obj viene salvato")


        if request.method == "POST":
            # some check that order is done

            is_done = order_obj.check_done()

            if is_done:
                order_obj.mark_paid()
                request.session["cart_items"] = 0
                del request.session["cart_id"]
                return redirect("cart:success")
            
    context = {

        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form" : guest_form,
        "address_form" : address_form,
        "address_qs":address_qs,        

    }

    return render(request, "carts/checkout.html", context )



def checkout_done_view(request):
    context = {}
    return render(request, "carts/checkout-done.html", context)