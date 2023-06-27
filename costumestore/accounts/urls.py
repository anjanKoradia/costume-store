from django.urls import path
from . import views

urlpatterns = [
    path("vendor/", views.VendorProfile.as_view(), name="vendor_profile"),
    path("vendor/address/", views.vendor_address, name="vendor_address"),
]
