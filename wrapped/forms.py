from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from wrapped.models import Feedback

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm

class FeedbackForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=20)
    last_name = forms.CharField(label="Last Name", max_length=20)
    email = forms.EmailField(label="Email")
    subject = forms.CharField(label="Subject", max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Feedback
        fields = ('first_name', 'last_name', 'email', 'subject', 'message')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AccountForm(forms.Form):
    username = forms.CharField(max_length=250, required=False)
    email = forms.EmailField(required=False)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    def clean(self):
        cleaned_data = super().clean()

        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if not current_password:
                raise ValidationError("Current password is required to change the password.")
            if new_password != confirm_password:
                raise ValidationError("New password and confirm password must match.")

        return cleaned_data


