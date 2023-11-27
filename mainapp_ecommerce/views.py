from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .forms import ContactForm

def home_page(request):
    
    print(request.session.get("first_name", "unknown"))

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
    "form": contact_form,
    "brand":"new brand name",
    }

    if contact_form.is_valid():
        print("contact_form.cleaned_data", contact_form.cleaned_data)
        
        if request.is_ajax(): # asinchronous javascript and xml
            print("Ajax request")
        
            # se la richiesta è ajax, devo ritornare dati usando il formato ajax -> jsonresponse
            # quindi lo aggiungo usando jsonresoonse
            dict_for_jsonresponse = {
                "message": "thanks!!"
            }
            return JsonResponse(dict_for_jsonresponse)
        
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))  
    # 
        else:
            print("no ajax in this request:", request) 

    if contact_form.errors:
        print(contact_form.cleaned_data)
        errors = contact_form.as_json()
        if request.is_ajax():
            return HttpResponse(errors, stauts=400, content_type='application/json')
            """ 
            NOTA:
            JsonResponse trasforma in json i dizionari python e poi fa la response,
            se l'oggetto che passo alla response è un json, allora posso usare direttamente la httpresponse,
            però devo anche indicare il conent-type come content_type='application/json'
            """

    return render(request, "contact/view.html", context )




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