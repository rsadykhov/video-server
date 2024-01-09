from . import models
from django import forms



class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password_validation = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={"placeholder":"Password"}),
                                          help_text="Enter the same password as above, for verification.")

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "username")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder":"First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder":"Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder":"Email"}),
            "username": forms.TextInput(attrs={"placeholder":"Username"}),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserSignUpForm, self).clean()
        password = cleaned_data.get("password")
        password_validation = cleaned_data.get("password_validation")
        if password and password_validation and password != password_validation:
            self.add_error("password_validation", "Passwords do not match.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user