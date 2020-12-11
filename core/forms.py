from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import PasswordInput
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'id_password',
        }))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'id_email',
        }
))

class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(max_length=128, widget=PasswordInput())

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','first_name','last_name', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class RegistrationForm(ModelForm):
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'Field','placeholder':'First Name'}))
    email= forms.CharField(max_length=100,widget= forms.EmailInput(attrs={'class':'Field','placeholder':'Email'}))   
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'Field','placeholder':'Last Name'}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'Field', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
    def save(self):
        username = email = self.cleaned_data.get('email')
        firstname = self.cleaned_data.get('first_name')
        lastname = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        return CustomUser.objects.create_user(email=email, password=password,firstname=firstname, lastname=lastname)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': PasswordInput()
        }

