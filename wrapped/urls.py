from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import IndexView, SignUpView, LogInView, LinkTokenView, ResetPasswordView, ResetPasswordConfirmView, DeveloperContactView, FeedbackView

app_name = 'wrapped'

urlpatterns = [
    path("link-token/", LinkTokenView.as_view(), name="link_token"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("reset/", ResetPasswordView.as_view(), name="reset_password"),
    path("reset/<uidb64>/<token>/", ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path("", IndexView.as_view(), name="home"),
    path("help/", DeveloperContactView.as_view(), name="developer"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
    path('', include('django.contrib.auth.urls')),


]