from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("store/", views.Store.as_view(), name="store"),
    path("orders/", views.Orders.as_view(), name="orders"),
    path("orders/update/status/", views.update_order_status, name="update_order_status"),
    path("add/product/",views.Add_Product.as_view(), name="add_product"),
    path("delete/<str:id>/", views.delete_product, name="delete_product"),
    path("edit/product/<str:id>/",views.Edit_Product.as_view(), name="edit_product"),
]
