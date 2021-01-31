from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model

from .forms import LoginForm, RegisterForm

# Create your views here.

def login_page(request):

    
    form = LoginForm(request.POST or None)
    context = {"form":form}

    print("User logged in: %s" % request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)  
        username = form.cleaned_data.get("username")  
        password = form.cleaned_data.get("password")    
        user = authenticate(request, username=username, password=password)
        print("User logged in: %s" % request.user.is_authenticated)

        if user is not None:
            login(request, user)
            # redirect to success page
            return redirect("/")
        else:
            #return invalid login error message
            print("invalid login")
    

    return render(request, "accounts/login.html", context)

User = get_user_model()


def register_page(request):

    form = RegisterForm(request.POST or None)
    context = {"form":form}

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")  
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    
    return render(request, "accounts/register.html", context)