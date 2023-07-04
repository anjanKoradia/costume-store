from django.contrib import admin
from django.urls import path, include, re_path
from common.views import error_404


urlpatterns = [
    path("", include("website.urls")),
    path("visitor/auth/", include("authentication.urls")),
    path("vendor/", include("vendor.urls")),
    path("account/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("payment/", include("payment.urls")),
    re_path(r'^.*$', error_404), 
]