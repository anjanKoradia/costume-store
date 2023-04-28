from django.urls import path
from . import views

urlpatterns = [
    path("", views.customer_auth_page, name="customer_auth_page"),
]
