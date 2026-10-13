"""
Management command to attach high-fidelity original vector assets to Products and Categories.
Run: python manage.py attach_assets
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product, Banner

PRODUCT_MAP = {
    'Luminex Pro 15': 'products/luminex_pro_15.svg',
    'Luminex Air 15': 'products/luminex_air_15.svg',
    'Luminex Mini 15': 'products/luminex_mini_15.svg',
    'Luminex Book Pro 16': 'products/luminex_book_pro_16.svg',
    'Luminex Book Air 15': 'products/luminex_book_air_15.svg',
    'Luminex Buds Pro 3': 'products/luminex_buds_pro_3.svg',
    'Luminex Phones Max': 'products/luminex_phones_max.svg',
    'Luminex Watch Ultra 2': 'products/luminex_watch_ultra_2.svg',
    'Luminex Watch Series 9': 'products/luminex_watch_series_9.svg',
    'Luminex Pad Pro 13"': 'products/luminex_pad_pro_13.svg',
    'Luminex MagCharge 30W': 'products/luminex_magcharge.svg',
    'Luminex Smart Folio': 'products/luminex_smart_folio.svg',
}

CAT_MAP = {
    'Smartphones': 'categories/cat_smartphones.svg',
    'Laptops': 'categories/cat_laptops.svg',
    'Audio': 'categories/cat_audio.svg',
    'Wearables': 'categories/cat_wearables.svg',
    'Tablets': 'categories/cat_tablets.svg',
    'Accessories': 'categories/cat_accessories.svg',
}

class Command(BaseCommand):
    help = 'Attach vector assets to products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Attaching assets to catalog...')
        for name, img_path in PRODUCT_MAP.items():
            prod = Product.objects.filter(name=name).first()
            if prod:
                prod.main_image = img_path
                prod.save()
                self.stdout.write(f'  ✓ Product: {name} -> {img_path}')

        for cat_name, img_path in CAT_MAP.items():
            cat = Category.objects.filter(name=cat_name).first()
            if cat:
                cat.image = img_path
                cat.save()
                self.stdout.write(f'  ✓ Category: {cat_name} -> {img_path}')

        # Attach to banners if relevant
        b1 = Banner.objects.filter(title='Luminex Pro 15').first()
        if b1:
            b1.image = 'products/luminex_pro_15.svg'
            b1.save()
        b2 = Banner.objects.filter(title='Luminex Book Pro 16').first()
        if b2:
            b2.image = 'products/luminex_book_pro_16.svg'
            b2.save()

        self.stdout.write(self.style.SUCCESS('All assets attached successfully.'))
