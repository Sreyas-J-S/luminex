"""
Cart management utilities for Luminex.
Handles guest sessions and authenticated user cart persistence and merge.
"""
from .models import Cart, CartItem, Product


def get_cart(request):
    """Retrieve existing cart for request without creating if empty."""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    if not request.session.session_key:
        return None
    return Cart.objects.filter(session_key=request.session.session_key).first()


def get_or_create_cart(request):
    """Retrieve or create an active cart for the current session or user."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # If there was a guest cart before logging in, merge it
        if request.session.session_key:
            guest_cart = Cart.objects.filter(session_key=request.session.session_key).exclude(pk=cart.pk).first()
            if guest_cart:
                for item in guest_cart.items.all():
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart, product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not created:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                guest_cart.delete()
        return cart

    # Guest user
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart
