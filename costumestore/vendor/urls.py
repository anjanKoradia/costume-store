from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("store/", views.Store.as_view(), name="store"),
    path("orders/", views.Orders.as_view(), name="orders"),
    path("orders/completed/", views.CompletedOrders.as_view(), name="completed_orders"),
    path("orders/update/status/", views.update_order_status, name="update_order_status"),
    path("product/add/",views.AddProduct.as_view(), name="add_product"),
    path("product/delete/<str:id>/", views.DeleteProduct.as_view(), name="delete_product"),
    path("edit/product/<str:id>/",views.EditProduct.as_view(), name="edit_product"),
]
