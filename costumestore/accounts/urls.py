from django.urls import path
from . import views

urlpatterns = [
    path("vendor/", views.VendorProfile.as_view(), name="vendor_profile"),
]
