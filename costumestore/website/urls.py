from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("visitor/contact/", views.contact_page, name="contact_page"),
    path("visitor/shop/<str:category>/", views.ShopPage.as_view(), name="shop_page"),
    path("visitor/product/<str:id>/", views.product_details, name="product_details"),
    # wishlist related routes
    path(
        "customer/wishlist/",
        views.WishlistOperations.wishlist_page,
        name="wishlist_page",
    ),
    path(
        "customer/wishlist/<str:operation>/<str:id>/",
        views.WishlistOperations.wishlist_operations,
        name="wishlist_operations",
    ),
    # cart related routes
    path("customer/cart/", views.CartOperations.cart_page, name="cart_page"),
    path(
        "customer/cart/add/<str:id>/",
        views.CartOperations.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "customer/cart/<str:operation>/<str:id>/",
        views.CartOperations.cart_item_qty,
        name="cart_item_qty",
    ),
    # order related routes
    path("customer/orders/", views.my_orders, name="my_orders"),
]
