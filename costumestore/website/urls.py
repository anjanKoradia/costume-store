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
        views.WishlistOperations.as_view(),
        name="wishlist",
    ),
    # cart related routes
    path("customer/cart/", views.CartOperations.as_view(), name="cart"),
    # order related routes
    path("customer/orders/", views.my_orders, name="my_orders"),
]
