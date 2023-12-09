from django import forms
from django.contrib.auth import get_user_model

# code from external guide
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # la widget mette gli asterischi nel campo passwrd a frontend


# copypaste from external guide -S
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email') #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['full_name']



class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
# copypaste from external guide - E


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

