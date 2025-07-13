from django.forms import ModelForm
from django import forms
from .models import UserDetails

class SignUpForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = "__all__"

class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
