"""
Store views for Luminex e-commerce platform.
Features: catalog, search, cart, checkout, inventory validation, and orders.
"""
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import Product, Category, Banner, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from .cart import get_or_create_cart, get_cart


def home(request):
    """Homepage with hero banners, featured products, categories and promos."""
    hero_banners = Banner.objects.filter(is_active=True, position='hero').order_by('sort_order')
    promo_banners = Banner.objects.filter(is_active=True, position='promo').order_by('sort_order')
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True).select_related('category')[:8]
    categories = Category.objects.filter(is_active=True).order_by('sort_order')[:8]
    audio_products = Product.objects.filter(is_active=True, category__slug='audio').order_by('price')[:4]
    accessories_products = Product.objects.filter(is_active=True, category__slug='accessories').order_by('price')[:4]

    context = {
        'hero_banners': hero_banners,
        'promo_banners': promo_banners,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'audio_products': audio_products,
        'accessories_products': accessories_products,
        'page_title': 'Luminex Store — The best way to buy products you love',
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """All products with search and category filtering."""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')

    products = Product.objects.filter(is_active=True).select_related('category')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        )

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=active_category)

    SORT_OPTIONS = {
        'price_asc': ('price', 'Price: Low to High'),
        'price_desc': ('-price', 'Price: High to Low'),
        '-created_at': ('-created_at', 'Newest First'),
        'name': ('name', 'Name A–Z'),
    }
    sort_field = SORT_OPTIONS.get(sort, ('-created_at', 'Newest First'))[0]
    products = products.order_by(sort_field)

    context = {
        'products': products,
        'query': query,
        'active_category': active_category,
        'sort': sort,
        'sort_options': SORT_OPTIONS,
        'total': products.count(),
        'page_title': f"{'Search: ' + query if query else (active_category.name if active_category else 'All Products')} | Luminex",
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Individual product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    gallery = product.images.all()
    related_products = Product.objects.filter(
        is_active=True,
        category=product.category
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'page_title': f"Buy {product.name} — Luminex",
    }
    return render(request, 'store/product_detail.html', context)


def category_detail(request, slug):
    """Products filtered by category."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    sort = request.GET.get('sort', '-created_at')
    SORT_OPTIONS = {
        'price_asc': ('price', 'Price: Low to High'),
        'price_desc': ('-price', 'Price: High to Low'),
        '-created_at': ('-created_at', 'Newest First'),
        'name': ('name', 'Name A–Z'),
    }
    sort_field = SORT_OPTIONS.get(sort, ('-created_at', 'Newest First'))[0]
    products = Product.objects.filter(
        is_active=True, category=category
    ).order_by(sort_field)

    context = {
        'category': category,
        'products': products,
        'sort': sort,
        'sort_options': SORT_OPTIONS,
        'total': products.count(),
        'page_title': f"{category.name} | Luminex",
    }
    return render(request, 'store/category_detail.html', context)


def search(request):
    """Redirect search to product list."""
    q = request.GET.get('q', '')
    return redirect(f'/products/?q={q}')


# ====================== CART & CHECKOUT ======================

def cart_detail(request):
    """Display shopping bag/cart."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    # Calculate free shipping eligibility (threshold ₹5,000)
    subtotal = cart.total_price
    free_shipping_threshold = 5000
    qualifies_free_shipping = subtotal >= free_shipping_threshold
    free_shipping_deficit = max(0, free_shipping_threshold - subtotal) if subtotal > 0 else free_shipping_threshold
    delivery_fee = 0 if qualifies_free_shipping else (499 if subtotal > 0 else 0)
    grand_total = subtotal + delivery_fee

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
        'qualifies_free_shipping': qualifies_free_shipping,
        'free_shipping_threshold': free_shipping_threshold,
        'free_shipping_deficit': free_shipping_deficit,
        'page_title': 'Review your Bag — Luminex',
    }
    return render(request, 'store/cart.html', context)


def cart_add(request, product_id):
    """Add item to shopping bag."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect(product.get_absolute_url())

    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1
    qty = max(1, qty)

    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        new_qty = cart_item.quantity + qty
        if new_qty > product.stock:
            messages.warning(
                request,
                f"Only {product.stock} units of {product.name} available in stock. Adjusted quantity."
            )
            cart_item.quantity = product.stock
        else:
            cart_item.quantity = new_qty
        cart_item.save()
    else:
        if qty > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            messages.warning(request, f"Added maximum available stock ({product.stock}) to your bag.")
        else:
            cart_item.quantity = qty
            cart_item.save()

    messages.success(request, f"Added {product.name} to your bag.")
    return redirect('store:cart_detail')


def cart_update(request, item_id):
    """Update quantity of an item in the bag."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            qty = int(request.POST.get('quantity', cart_item.quantity))
        except (ValueError, TypeError):
            qty = cart_item.quantity

        if action == 'increase':
            qty = cart_item.quantity + 1
        elif action == 'decrease':
            qty = cart_item.quantity - 1

        if qty <= 0:
            cart_item.delete()
            messages.info(request, f"Removed {cart_item.product.name} from your bag.")
        elif qty > cart_item.product.stock:
            cart_item.quantity = cart_item.product.stock
            cart_item.save()
            messages.warning(request, f"Maximum available stock for {cart_item.product.name} is {cart_item.product.stock}.")
        else:
            cart_item.quantity = qty
            cart_item.save()
            messages.success(request, "Bag updated.")

    return redirect('store:cart_detail')


def cart_remove(request, item_id):
    """Remove item from cart."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed {product_name} from your bag.")
    return redirect('store:cart_detail')


def checkout(request):
    """Checkout view with server-side validation, idempotency, and stock deduction."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        # Handle repeated submission / browser back: redirect to completed order if available
        last_order = request.session.get('last_order_number')
        if last_order:
            return redirect('store:order_confirmation', order_number=last_order)
        messages.warning(request, "Your bag is empty. Please add items before proceeding to checkout.")
        return redirect('store:product_list')

    # Server-side validation of active status and stock
    for item in cart_items:
        if not item.product.is_active or item.product.stock < item.quantity:
            messages.error(
                request,
                f"Sorry, {item.product.name} has only {item.product.stock} items in stock. Please adjust your bag."
            )
            return redirect('store:cart_detail')

    subtotal = cart.total_price
    delivery_fee = 0 if subtotal >= 5000 else 499
    grand_total = subtotal + delivery_fee

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    # Generate or reuse checkout nonce for idempotency
    checkout_nonce = request.session.get('checkout_nonce')
    if not checkout_nonce:
        checkout_nonce = uuid.uuid4().hex
        request.session['checkout_nonce'] = checkout_nonce

    if request.method == 'POST':
        submitted_nonce = request.POST.get('checkout_nonce')
        # If this exact checkout submission was already processed, redirect safely to the order
        if submitted_nonce and submitted_nonce == request.session.get('completed_checkout_nonce'):
            last_order = request.session.get('last_order_number')
            if last_order:
                return redirect('store:order_confirmation', order_number=last_order)

        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Lock cart row to prevent concurrent processing of the same cart
                locked_cart = Cart.objects.select_for_update().get(pk=cart.pk)
                current_cart_items = list(locked_cart.items.select_for_update().select_related('product').all())

                if not current_cart_items:
                    last_order = request.session.get('last_order_number')
                    if last_order:
                        return redirect('store:order_confirmation', order_number=last_order)
                    messages.warning(request, "Your bag is empty.")
                    return redirect('store:product_list')

                # Sort cart items by product_id for deterministic row locking order across concurrent transactions (PostgreSQL deadlock prevention)
                current_cart_items.sort(key=lambda it: it.product_id)

                # Re-validate stock with row-level locks
                locked_products = {}
                for item in current_cart_items:
                    prod = Product.objects.select_for_update().get(pk=item.product.pk)
                    if prod.stock < item.quantity:
                        messages.error(request, f"Insufficient stock for {prod.name}. Please review your bag.")
                        return redirect('store:cart_detail')
                    locked_products[item.product.pk] = prod

                # Create Order
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                else:
                    guest_orders = request.session.get('guest_orders', [])
                    if order.order_number not in guest_orders:
                        guest_orders.append(order.order_number)
                    request.session['guest_orders'] = guest_orders

                order.total_amount = grand_total
                order.status = 'processing'
                order.save()

                # Create OrderItems and safely deduct stock
                for item in current_cart_items:
                    prod = locked_products[item.product.pk]
                    OrderItem.objects.create(
                        order=order,
                        product=prod,
                        product_name=prod.name,
                        price=prod.price,
                        quantity=item.quantity
                    )
                    prod.stock = max(0, prod.stock - item.quantity)
                    prod.save()

                # Clear cart items
                locked_cart.items.all().delete()

                # Record idempotency and last order in session
                request.session['last_order_number'] = order.order_number
                if submitted_nonce:
                    request.session['completed_checkout_nonce'] = submitted_nonce
                request.session.pop('checkout_nonce', None)
                request.session.modified = True

            messages.success(request, f"Thank you! Your order #{order.order_number} has been placed successfully.")
            return redirect('store:order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, "Please check the information entered below.")
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
        'checkout_nonce': checkout_nonce,
        'page_title': 'Checkout — Luminex',
    }
    return render(request, 'store/checkout.html', context)


def order_confirmation(request, order_number):
    """Order confirmation and receipt with strict ownership & session verification."""
    order = get_object_or_404(Order, order_number=order_number)

    # Permission verification:
    # 1. Staff users can inspect any order
    # 2. Authenticated user who placed the order can view it
    # 3. Guest user whose active session placed the order can view it
    has_permission = False
    if request.user.is_staff:
        has_permission = True
    elif order.user is not None:
        if request.user.is_authenticated and request.user == order.user:
            has_permission = True
    else:
        # Guest order: verify order_number in session guest_orders
        guest_orders = request.session.get('guest_orders', [])
        if order.order_number in guest_orders:
            has_permission = True

    if not has_permission:
        return HttpResponseForbidden("You do not have permission to view this order confirmation.")

    context = {
        'order': order,
        'page_title': f"Order #{order.order_number} Confirmed — Luminex",
    }
    return render(request, 'store/order_confirmation.html', context)
