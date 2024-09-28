from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SimpleUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'placeholder': 'Username'})
        }
