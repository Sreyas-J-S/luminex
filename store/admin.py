"""
Store admin configuration - rich admin dashboard for Luminex.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Banner, Cart, CartItem, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text', 'sort_order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return "No image"
    preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order', 'product_count', 'thumbnail')
    list_editable = ('is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('sort_order', 'name')

    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = "Active Products"

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    thumbnail.short_description = "Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'original_price', 'stock',
        'is_active', 'is_featured', 'is_new_arrival', 'thumbnail', 'created_at'
    )
    list_editable = ('price', 'stock', 'is_active', 'is_featured', 'is_new_arrival')
    list_filter = ('category', 'is_active', 'is_featured', 'is_new_arrival')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('sku', 'created_at', 'updated_at', 'main_image_preview')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'sku', 'category', 'short_description', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'original_price', 'stock')
        }),
        ('Media', {
            'fields': ('main_image', 'main_image_preview')
        }),
        ('Visibility', {
            'fields': ('is_active', 'is_featured', 'is_new_arrival')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.main_image.url)
        return "—"
    thumbnail.short_description = "Image"

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.main_image.url)
        return "No image uploaded"
    main_image_preview.short_description = "Current Image Preview"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'position', 'is_active', 'sort_order',
        'cta_text', 'banner_preview', 'updated_at'
    )
    list_editable = ('is_active', 'sort_order', 'position')
    list_filter = ('position', 'is_active')
    search_fields = ('title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at', 'banner_preview')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_link')
        }),
        ('Media & Styling', {
            'fields': ('image', 'banner_preview', 'bg_color', 'text_color')
        }),
        ('Display Settings', {
            'fields': ('position', 'is_active', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def banner_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px;" />', obj.image.url)
        return "No image"
    banner_preview.short_description = "Preview"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'subtotal')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'total_items', 'formatted_total', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'full_name', 'email', 'formatted_total',
        'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('order_number', 'full_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'formatted_total')
    inlines = [OrderItemInline]

