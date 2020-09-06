from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.EmailInput()
    )

    first_name = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'placeholder': 'For example: Ahmed',
            }
        )
    )

    last_name = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'placeholder': 'For example: Alaa',
            }
        )
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


