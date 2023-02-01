from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label='Password confirmation', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = { 'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={ 'autofocus':True , 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, 
                widget=forms.PasswordInput(attrs={ 'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    old_password = forms.CharField(label=_('Old password'), 
        widget=forms.PasswordInput(attrs={ 'autofocus':True , 'class': 'form-control'}))

    new_password1 = forms.CharField(label=_('New password'), strip=False,
        widget=forms.PasswordInput(attrs=
        { 'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_('New password confirmation'), strip=False,
        widget=forms.PasswordInput(attrs=
        { 'type': 'password', 'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'mail', 'class': 'form-control'}))
    
class MySetPasswordForm(SetPasswordForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_('New password'), strip=False,
        widget=forms.PasswordInput(attrs=
        { 'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_('New password confirmation'), strip=False,
        widget=forms.PasswordInput(attrs=
        { 'type': 'password', 'class': 'form-control'}))








