from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("cart/", views.cart_page, name="cart_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("shop/<str:category>/", views.Shop_Page.as_view(), name="shop_page"),
    path("product/<str:id>/", views.product_details, name="product_details"),
]
