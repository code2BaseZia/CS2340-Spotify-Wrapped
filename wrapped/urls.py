from django.urls import path, include

from .views import IndexView, SignUpView, LogInView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("", IndexView.as_view(), name="home"),
    path('', include('django.contrib.auth.urls')),
]