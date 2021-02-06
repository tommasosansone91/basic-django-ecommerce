from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model

from .forms import LoginForm, RegisterForm

from django.utils.http import is_safe_url

from .forms import GuestForm

from .models import GuestEmail

# Create your views here.

def guest_register_view(request):    

    form = GuestForm(request.POST or None)
    context = {"form":form}

    print("User logged in: %s" % request.user.is_authenticated)

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        # redirect to success page
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register")

    return redirect("/register")



def login_page(request):

    
    form = LoginForm(request.POST or None)
    context = {"form":form}

    print("User logged in: %s" % request.user.is_authenticated)

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if form.is_valid():
        print(form.cleaned_data)  
        username = form.cleaned_data.get("username")  
        password = form.cleaned_data.get("password")    
        user = authenticate(request, username=username, password=password)
        print("User logged in: %s" % request.user.is_authenticated)

        if user is not None:
            login(request, user)

            try:
                del request.session['guest_email_id']
            except:
                pass
            

            # redirect to success page
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")

            return redirect("/")

            """
            in questo modo se faccio

            http://127.0.0.1:8000/login/?next=/cart/checkout

            una volta che ho passato la login finisco direttamente al cart/checkout
            """

        else:
            #return invalid login error message
            print("invalid login")
    

    return render(request, "accounts/login.html", context)

User = get_user_model()


def register_page(request):

    form = RegisterForm(request.POST or None)
    context = { "form":form }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")  
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    
    return render(request, "accounts/register.html", context)