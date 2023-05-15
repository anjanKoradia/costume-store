from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/product/",views.Add_Product.as_view(), name="add_product"),
    path("edit/product/<str:id>/",views.Edit_Product.as_view(), name="edit_product"),
]
