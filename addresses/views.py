from django.shortcuts import render, redirect

from .forms import AddressForm
from django.utils.http import url_has_allowed_host_and_scheme

from billing.models import BillingProfile

from .models import Address

# Create your views here.
def checkout_address_create_view(request):

    form = AddressForm(request.POST or None)
    context = {"form":form}

    # print("User logged in: %s" % request.user.is_authenticated)

    next_ = request.GET.get('next')
    print("---> next_ = request.GET.get('next')")
    print(next_)

    next_post = request.POST.get('next')
    print("---> next_post = request.POST.get('next')")
    print(next_post)

    redirect_path = next_ or next_post or None
    print("---> redirect_path = next_ or next_post or None")
    print(redirect_path)

    if form.is_valid():
        print("form is valid")
        print(request.POST)
        instance = form.save(commit=False)
        
        # qui mi ha fatto togliere l'altro er errore
        # cannot unpack non-iterable BillingProfile object
        billing_profile = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type +  "_address_id"] = instance.id
            print(address_type +  "_address_id")

        else:
            print("error here smth")
            return redirect("cart:checkout")

        # redirect to success page
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        

    else:
        print("form is not valid")

    return redirect("cart:checkout")




def checkout_address_reuse_view(request):

    if request.user.is_authenticated:
        
        context = {}

        next_ = request.GET.get('next')
        print("---> next_ = request.GET.get('next')")
        print(next_)

        next_post = request.POST.get('next')
        print("---> next_post = request.POST.get('next')")
        print(next_post)

        redirect_path = next_ or next_post or None
        print("---> redirect_path = next_ or next_post or None")
        print(redirect_path)

        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)

            address_type = request.POST.get('address_type', 'shipping')
            billing_profile = BillingProfile.objects.new_or_get(request)

            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type +  "_address_id"] = shipping_address
            
            # print(address_type +  "_address_id")

            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)

    return redirect("cart:checkout")