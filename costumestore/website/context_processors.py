from .models import CartItem, WishlistItem
from django.contrib.auth.decorators import login_required


def custom_context_processor(request):
    cart_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).count()

    # Return the data as a dictionary
    return {"cart_count": cart_count, "wishlist_count": wishlist_count}
