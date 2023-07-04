from website.models import CartItem, WishlistItem

def custom_context_processor(request):
    """
    Custom context processor to add cart and wishlist counts to the context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the cart and wishlist counts.
    """
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).count()

    # Return the data as a dictionary
    return {"cart_count": cart_count, "wishlist_count": wishlist_count}
