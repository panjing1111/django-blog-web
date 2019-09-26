from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# 用户注册时候的表单 目的是自带的username
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone",)