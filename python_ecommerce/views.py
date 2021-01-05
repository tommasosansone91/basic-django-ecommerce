from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):

    context = {
    "title":"Home",
    "content":"Welcome to the home page",
    "premium_content":"yeah!",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "Premiuim Yeahhhh"

    return render(request, "home.html", context )

def about_page(request):

    context = {
        "title":"About",
        "content":"Welcome to the about page!"
        }

    return render(request, "about.html", context )

def contact_page(request):

    contact_form = ContactForm(request.POST or None)
    # None, dice "if there is not, then pass not"

    context = {
    "title":"Contact",
    "content":"Welcome to the contact page!",
    "form":contact_form,
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))       

    return render(request, "contact/view.html", context )

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
    

    return render(request, "auth/login.html", context)

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
    
    return render(request, "auth/register.html", context)


"""
https://docs.djangoproject.com/en/3.1/topics/auth/default/
Creating users¶
The most direct way to create users is to use the included create_user() helper function:

>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
>>> user.last_name = 'Lennon'
>>> user.save()
If you have the Django admin installed, you can also create users interactively.
"""