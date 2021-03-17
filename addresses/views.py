from django.shortcuts import render, redirect

from .forms import AddressForm
from django.utils.http import is_safe_url

from billing.models import BillingProfile

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
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        

    else:
        print("form is not valid")

    return redirect("cart:checkout")