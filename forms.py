from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'), 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label=_('Confirm Password'), 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'required': _('Email is required')}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': _('Email')
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=_('Password'), 
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'})
    )


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Old Password'), 
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_('New Password'), 
        strip=False,  
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'), 
        strip=False,  
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'), 
        max_length=255, 
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
        error_messages={'required': _('Email is required')}
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_('New Password'), 
        strip=False,  
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'), 
        strip=False,  
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Full Name'),
            'locality': _('Locality'),
            'city': _('City'),
            'state': _('State'),
            'zipcode': _('Zip Code'),
        }
        help_texts = {
            'zipcode': _('Please enter a valid 6-digit postal code.'),
        }
