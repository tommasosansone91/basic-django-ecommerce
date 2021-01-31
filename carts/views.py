from django.shortcuts import render, redirect

# Create your views here.

from products.models import Product
from .models import Cart

from orders.models import Order

# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('new cart created')
#     return cart_obj

def cart_home(request):

# faccio tutto coi signals e receiver
    # cart_obj, new_obj = Cart.objects.new_or_get(request)


    # # cart_id = request.session.get("cart_id", None)

    # # # # isinstance(cart_id, int) è per assicurarsi che il termine 1 sia del tipo dl termine 2
    # # # if cart_id is None and isinstance(cart_id, int):        

    # # qs = Cart.objects.filter(id=cart_id)
    # # if qs.count()==1:
    # #     print('Cart ID exists')
    # #     cart_obj=qs.first()
    # #     if request.user.is_authenticated and cart_obj.user is None:
    # #         cart_obj.user = request.user
    # #         cart_obj.save()

        
    # # else:        
    # #     cart_obj = Cart.objects.new(user=request.user)
    # #     request.session['cart_id']=cart_obj.id
            
    # # # print(request.session) #
    # # # print(dir(request.session)) # dir mi mostra tutti i metodi di un modulo

    # products = cart_obj.products.all()

    # total = 0
    # for x in products:
    #     total += x.price

    # print("total")
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()



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
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "carts/checkout.html", {"order":order_obj} )