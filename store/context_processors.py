"""
Context processors for Luminex store.
Makes categories available in all templates.
"""
from .models import Category
from .cart import get_cart


def categories(request):
    """Inject active categories and cart count into every template context."""
    cart = get_cart(request)
    total_items = cart.total_items if cart else 0
    return {
        'nav_categories': Category.objects.filter(is_active=True).prefetch_related('products').order_by('sort_order', 'name'),
        'cart_item_count': total_items,
        'cart': cart,
    }

