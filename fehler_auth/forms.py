from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from django import forms

from .models import User, Invite


class EmailLowerField(forms.EmailField):
    def to_python(self, value):
        return value.lower()


# class UserRegisterForm(UserCreationForm):
#     email = EmailLowerField(required=True, label='email', widget=forms.EmailInput(attrs={'class': 'email__input form__input', 'placeholder': 'jon@example.com'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password__input form__input', 'placeholder': '●●●●●●●●●●'}))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'first__input form__input', 'placeholder': 'Jon'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'last__input form__input', 'placeholder': 'Smith'}))

#     def __init__(self, *args, **kwargs):
#         super(UserRegisterForm, self).__init__(*args, **kwargs)
#         self.fields.pop('password2')

#     class Meta:
#         model = User
#         fields = ['email', 'password1', 'first_name', 'last_name']


# class UserAuthForm(AuthenticationForm):
#     username = EmailLowerField(required=True, label='email', widget=forms.EmailInput(attrs={'class': 'email__input form__input', 'placeholder': 'jon@example.com'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password__input form__input', 'placeholder': '●●●●●●●●●●'}))

#     class Meta:
#         model = User
#         fields = ['email', 'password']


class UserInviteForm(forms.ModelForm):
    email = EmailLowerField(
        required=True,
        label="email",
        widget=forms.TextInput(attrs={"placeholder": "john@example.com"}),
    )

    class Meta:
        model = Invite
        fields = ["email", "member_type"]


class UserInviteRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "●●●●●●●●●●"})
    )

    class Meta:
        model = User
        fields = ["password"]


# from django import forms
# from django.forms import ModelForm

# from . models import Organistion, SpaceMembership
# from fehler_auth.forms import EmailLowerField


# class OrgCreationForm(ModelForm):
#     name = forms.CharField(required=True, label='email', widget=forms.TextInput(attrs={'class': 'space__input form__input', 'placeholder': 'Fehler'}))

#     def clean_name(self):
#         name = self.cleaned_data['name']
#         return name.lower()

#     class Meta:
#         model = Organistion
#         fields = ['name']
