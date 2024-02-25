from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class  CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='User Name',widget=forms.TextInput(attrs={ 'class': 'form-control','placeholder':'Enter the UserName'}))
    email = forms.EmailField(label= 'E-mail Address',required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter the Email Address'}))
    password1 = forms.CharField(label='Password',required= True, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password', 'class':"form-control"}))
    password2 = forms.CharField(label='Confirm password',required=True, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password', 'class':"form-control"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']