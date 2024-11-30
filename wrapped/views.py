from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView, FormView, DetailView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from api.serializers import WrappedSerializer
from api.util import get_wrap_by_id
from .forms import FeedbackForm, CustomUserCreationForm, AccountForm
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from .models import Feedback, SpotifyUserWrap
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib import messages
from django.utils import dateparse
from django.http.response import Http404

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
        context = WrappedSerializer(SpotifyUserWrap.objects.first(), context={'request': self.request}).data
        context['owner'] = context['user']
        context['user'] = self.request.user

        if self.request.user.is_authenticated and self.request.user.profile.token is not None:
            context['linked'] = True
        else:
            context['linked'] = False

        return context


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


class AccountView(TemplateView, FormView):
    template_name = "wrapped/pages/account.html"
    form_class = AccountForm
    success_url = reverse_lazy("wrapped:account")
    success_message = "Account settings updated successfully."

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        current_password = form.cleaned_data['current_password']
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']

        if username and username != user.username:
            user.username = username
        if email and email != user.email:
            user.email = email

        if current_password or new_password or confirm_password:
            if not (current_password and new_password and confirm_password):
                messages.error(self.request, 'Please fill in all password fields to change your password.')
                return self.form_invalid(form)

            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    update_session_auth_hash(self.request, user)
                else:
                    messages.error(self.request, 'The new passwords do not match.')
                    return self.form_invalid(form)
            else:
                messages.error(self.request, 'Your current password was entered incorrectly.')
                return self.form_invalid(form)

        user.save()
        messages.success(self.request, "Your account information has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['email'] = self.request.user.email
        return context

    def post(self, request, *args, **kwargs):
        if "delete_account" in request.POST:
            return self.delete_account()
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def delete_account(self):
        user = self.request.user
        user.delete()
        logout(self.request)
        return redirect(reverse_lazy('wrapped:home'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class WrappedView(DetailView):
    model = SpotifyUserWrap
    template_name = 'wrapped/pages/wrap.html'

    def get_object(self, queryset=None):
        obj = super().get_queryset().first()

        if obj.user.user != self.request.user and not obj.public:
            raise Http404("This wrapped is private or does not exist")

        return obj

    def get_context_data(self, **kwargs):
        context = WrappedSerializer(self.object, context={'request': self.request}).data
        context['owner'] = context['user']
        context['user'] = self.request.user
        return context

class SavedView(ListView):
    template_name = 'wrapped/pages/saved.html'

    def get_context_data(self, **kwargs):
        object_list = []
        for object in self.object_list:
            serialized = WrappedSerializer(object, context={'request': self.request}).data
            serialized['created_at'] = dateparse.parse_datetime(serialized['created_at'])
            object_list.append(serialized)
        context = {'wraps': object_list}

        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return self.request.user.profile.wraps.all()


class DeleteWrappedView(DeleteView):
    model = SpotifyUserWrap
    success_url = reverse_lazy('wrapped:saved')