from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=200)

    class Meta:
        model = User
        # model = Customer
        fields = ['name', 'username', 'email', 'password1', 'password2']



class NameForm(forms.Form):
    your_name = forms.CharField(label='your-name', max_length=100)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class ContactusForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=500, required=True)
