from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import IndexView, SignUpView, LogInView, LinkTokenView, ResetPasswordView, ResetPasswordConfirmView, \
    DeveloperContactView, FeedbackView, AccountView, WrappedView, SavedView, DeleteWrappedView

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
    path("account/", AccountView.as_view(), name="account"),
    path("wrap/<int:pk>", WrappedView.as_view(), name="wrap"),
    path("wrap/<int:pk>/delete", DeleteWrappedView.as_view(), name="delete"),
    path('', include('django.contrib.auth.urls')),
    path("saved/", SavedView.as_view(), name="saved"),

]