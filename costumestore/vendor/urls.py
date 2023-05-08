from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/product/",views.Add_Product.as_view(), name="add_product"),
]
