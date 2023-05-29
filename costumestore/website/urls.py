from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("cart/", views.Cart_Operations.cart_page, name="cart_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("add-to-cart/<str:id>", views.Cart_Operations.add_to_cart, name="add_to_cart"),
    path("shop/<str:category>/", views.Shop_Page.as_view(), name="shop_page"),
    path("product/<str:id>/", views.product_details, name="product_details"),
    path(
        "cart/decrease-quantity/<str:id>",
        views.Cart_Operations.decrease_cart_item_qty,
        name="decrease_cart_item_qty",
    ),
    path(
        "cart/increase-quantity/<str:id>",
        views.Cart_Operations.increase_cart_item_qty,
        name="increase_cart_item_qty",
    ),
]
