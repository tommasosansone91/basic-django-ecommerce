from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField()


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


    """
    metodo preimpostato per aggiungere controlli custom nei django form.
    nella classe che eredita da (forms.Form), inserisco
    clean_ seguito dalla variabile su cui voglio eseguire i controlli
    ad esempio clean_content
    """

