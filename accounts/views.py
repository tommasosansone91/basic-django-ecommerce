from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model

from .forms import LoginForm, RegisterForm

from django.utils.http import url_has_allowed_host_and_scheme

from .forms import GuestForm

from .models import GuestEmail

from django.views.generic import CreateView, FormView

from .forms  import LoginForm

# Create your views here.

def guest_register_view(request):    

    form = GuestForm(request.POST or None)
    context = {"form":form}

    print("User logged in: %s" % request.user.is_authenticated)
    print("guest register")

    next_ = request.GET.get('next')
    print("next_ = request.GET.get('next')")
    print(next_)

    next_post = request.POST.get('next')
    print("next_post = request.POST.get('next')")
    print(next_post)

    redirect_path = next_ or next_post or None
    print("redirect_path = next_ or next_post or None")
    print(redirect_path)

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        # redirect to success page
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register")

    return redirect("/register")


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    # these must be given to the class

    def form_valid(self, form):

        print(form.cleaned_data)  

        request = self.request  # è un attributo ereditato da FormView

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post


        email = form.cleaned_data.get("username")  
        password = form.cleaned_data.get("password")    
        user = authenticate(request, username=email, password=password)

        print("User logged in: %s" % request.user.is_authenticated)

        if user is not None:
            login(request, user)

            try:
                del request.session['guest_email_id']
            except:
                pass
            # redirect to success page
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
            
        return super(LoginView, self).form_invalid(form)
            

            

# def login_page(request):
    
#     form = LoginForm(request.POST or None)
#     context = {"form":form}

#     print("User logged in: %s" % request.user.is_authenticated)
#     print("login_page")

#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post

#     if form.is_valid():
#         print(form.cleaned_data)  
#         username = form.cleaned_data.get("username")  
#         password = form.cleaned_data.get("password")    
#         user = authenticate(request, username=username, password=password)
#         print("User logged in: %s" % request.user.is_authenticated)

#         if user is not None:
#             login(request, user)

#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
            

#             # redirect to success page
#             if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")

#             return redirect("/")

#             """
#             in questo modo se faccio

#             http://127.0.0.1:8000/login/?next=/cart/checkout

#             una volta che ho passato la login finisco direttamente al cart/checkout
#             """

#         else:
#             #return invalid login error message
#             print("invalid login")
    

#     return render(request, "accounts/login.html", context)



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'
    # questi servono alla CreateView da cui eredita

    # in questo modo, tutto il User = get_user_model() e  def register_page(request): non servono piu

# User = get_user_model()

# def register_page(request):

#     form = RegisterForm(request.POST or None)
#     context = { "form":form }

#     if form.is_valid():
#         # print(form.cleaned_data)
#         # username = form.cleaned_data.get("username")  
#         # password = form.cleaned_data.get("password")
#         # email = form.cleaned_data.get("email")
#         # new_user = User.objects.create_user(username, email, password)
#         # print(new_user)

#         form.save()  
#         # posso mettere questo e commentare quello che c'era pri a perchè nei form ho messo
#         # class RegisterForm(forms.ModelForm):
#         #  con un suo metodo save
    
#     return render(request, "accounts/register.html", context)