from django.urls import path
from . import views

urlpatterns = [
    path("", views.Auth.as_view(), name="auth"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("activate/<email_token>", views.activate_user, name="activate"),
]
