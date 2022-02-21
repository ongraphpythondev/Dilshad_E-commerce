
from pyexpat import model
from .models import Customer, Profile
from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate

User = get_user_model()

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.
    PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='confirm password',widget=forms.
    PasswordInput(attrs={'class':'form-control'}))
    mobile = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,widget=forms.
    EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(required=True,widget=forms.
    TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        labels = {'email':'Email'}

class ProfileViewForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city', 'pincode','state']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'})
            }

class LoginForm(forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,
      'class': 'form-control'}))
    #username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True,'class': 'form-control'}))
    password = forms.CharField(label=_("password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
     'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','password']



class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'autofocus':True, 'class': 'form-control'}))

    new_password1 = forms.CharField(label=_("New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
     'class': 'form-control'}),
     help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
     'class': 'form-control'}))
    
class MyPasswordReset(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=254,widget=forms.
    EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
     'class': 'form-control'}),
     help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
     'class': 'form-control'}))

