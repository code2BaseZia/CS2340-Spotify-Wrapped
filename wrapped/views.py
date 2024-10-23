from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, RedirectView
from .models import Profile


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


# Create your views here.
class IndexView(TemplateView):
    template_name = 'wrapped/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.profile.token is not None:
            return {'linked': True}
        return {'linked': False}


class LogInView(LoginView):
    template_name = "wrapped/login.html"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("wrapped:login")
    template_name = "wrapped/signup.html"


class WrappedRedirectView(RedirectView):
    url = reverse_lazy("wrapped:home")


class LinkTokenView(TemplateView):
    template_name = "wrapped/linking.html"
