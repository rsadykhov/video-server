from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField



class UserLogInForm(AuthenticationForm):
    username = UsernameField(label="Username", widget=forms.TextInput(attrs={"placeholder":"Username", "class":"custom-form-field"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder":"Password", "class":"custom-form-field"}))