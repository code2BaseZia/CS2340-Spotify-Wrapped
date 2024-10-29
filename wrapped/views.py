from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import FeedbackForm, CustomUserCreationForm
from django.http import HttpResponseRedirect

from .models import Feedback

"""def get_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse_lazy("/thanks/"))
    else:
        form = FeedbackForm()

    return render(request, "wrapped/pages/feedback.html", {"form": form})
"""

class FeedbackView(CreateView, SuccessMessageMixin):
    form_class = FeedbackForm
    success_url = reverse_lazy("wrapped:feedback")
    success_message = "Your feedback has been recorded. We will get back to you shortly. o7"
    template_name = "wrapped/pages/feedback.html"


# Create your views here.
class IndexView(TemplateView):
    template_name = 'wrapped/pages/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.profile.token is not None:
            return {'linked': True}
        return {'linked': False}

class LogInView(LoginView):
    template_name = "wrapped/auth/login.html"


class SignUpView(CreateView, SuccessMessageMixin):
    form_class = CustomUserCreationForm
    success_message = "You have successfully registered."
    success_url = reverse_lazy("wrapped:login")
    template_name = "wrapped/auth/signup.html"


class ResetPasswordView(PasswordResetView, SuccessMessageMixin):
    template_name = "wrapped/auth/password_reset.html"
    email_template_name = "wrapped/email/password_reset_email.html"
    subject_template_name = "wrapped/email/password_reset_subject.txt"
    success_url = reverse_lazy("wrapped:login")
    success_message = "A link to reset your password has been sent to your email."


class ResetPasswordConfirmView(PasswordResetConfirmView, SuccessMessageMixin):
    template_name = "wrapped/auth/password_reset_confirm.html"
    success_message = "Your password was reset successfully."


class WrappedRedirectView(RedirectView):
    url = reverse_lazy("wrapped:home")


class LinkTokenView(TemplateView):
    template_name = "wrapped/pages/linking.html"


class DeveloperContactView(TemplateView):
    template_name = "wrapped/pages/help.html"