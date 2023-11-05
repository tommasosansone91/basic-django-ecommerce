from django import forms


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

