from django.urls import path, include
from .views import IndexView, SignUpView, LogInView, LinkTokenView

app_name = 'wrapped'

urlpatterns = [
    path("link-token/", LinkTokenView.as_view(), name="link_token"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("", IndexView.as_view(), name="home"),
    path('', include('django.contrib.auth.urls')),
]