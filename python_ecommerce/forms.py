from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    # eredita dalla classe form di django

    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder":"Your full name", 
                "id":"form_full_name"
                }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", 
                "placeholder":"Your email", 
                }
        )
    )
    

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 
                "placeholder":"Your content goes here...", 
                }
        )
    )

    """
    metodo preimpostato per aggiungere controlli custom nei django form.
    nella classe che eredita da (forms.Form), inserisco
    clean_ seguito dalla variabile su cui voglio eseguire i controlli
    ad esempio clean_content
    """

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # la widget mette gli asterischi nel campo passwrd a frontend


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) # la widget mette gli asterischi nel campo passwrd a frontend
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput) # la widget mette gli asterischi nel campo passwrd a frontend

    def clean_username(self):
        # si applica a user
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        print(qs)
        if qs.exists():
            raise forms.ValidationError("username is already taken")
        return username


    def clean_email(self):
        # si applica a user
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        print(qs)
        if qs.exists():
            raise forms.ValidationError("email is already taken")
        return email


    def clean(self):
        # si aplica a ??? tutti i dati
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("passwords must match.")
        return data