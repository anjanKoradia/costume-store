from .models import CartItem, WishlistItem


def custom_context_processor(request):
    cart_count = CartItem.objects.filter(cart__user=request.user).count()
    wishlist_count = WishlistItem.objects.filter(wishlist__user=request.user).count()

    # Return the data as a dictionary
    return {"cart_count": cart_count, "wishlist_count": wishlist_count}
