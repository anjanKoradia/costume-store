from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("visitor/contact/", views.contact_page, name="contact_page"),
    path("visitor/shop/<str:category>/", views.Shop_Page.as_view(), name="shop_page"),
    path("visitor/product/<str:id>/", views.product_details, name="product_details"),
    path(   
        "customer/wishlist/add/<str:id>/",
        views.Wishlist_Operations.add,
        name="add_to_wishlist",
    ),
    path(
        "customer/wishlist/remove/<str:id>/",
        views.Wishlist_Operations.remove,
        name="remove_from_wishlist",
    ),
    path("customer/cart/", views.Cart_Operations.cart_page, name="cart_page"),
    path(
        "customer/cart/add/<str:id>/",
        views.Cart_Operations.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "customer/cart/<str:operation>/<str:id>/",
        views.Cart_Operations.cart_item_qty,
        name="cart_item_qty",
    )
]
