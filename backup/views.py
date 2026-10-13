"""
Store views for Luminex e-commerce platform.
"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Banner


def home(request):
    """Homepage with hero banners, featured products, categories and promos."""
    hero_banners = Banner.objects.filter(is_active=True, position='hero').order_by('sort_order')
    promo_banners = Banner.objects.filter(is_active=True, position='promo').order_by('sort_order')
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True).select_related('category')[:8]
    categories = Category.objects.filter(is_active=True).order_by('sort_order')[:6]

    context = {
        'hero_banners': hero_banners,
        'promo_banners': promo_banners,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'page_title': 'Luminex — Illuminate Your World',
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
        'page_title': f"{product.name} | Luminex",
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
    from django.shortcuts import redirect
    q = request.GET.get('q', '')
    return redirect(f'/products/?q={q}')
