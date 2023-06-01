from django.urls import path
from . import views

urlpatterns = [
    path("vendor/", views.Vendor_Profile.as_view(), name="vendor_profile"),
    path("vendor/address/", views.vendor_address, name="vendor_address"),
]
