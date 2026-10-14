"""
Management command to seed demo data for Luminex store.
Run: python manage.py seed_demo
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from store.models import Category, Product, Banner


class Command(BaseCommand):
    help = 'Safely and idempotently seeds the database with demo categories, products, and banners'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Luminex demo data...')

        # --- Superuser ---
        if settings.DEBUG or os.getenv('RENDER') or os.getenv('ADMIN_USERNAME'):
            admin_user = os.getenv('ADMIN_USERNAME', 'admin')
            admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@luminex.com')

            user = User.objects.filter(username=admin_user).first()
            if not user:
                User.objects.create_superuser(admin_user, admin_email, admin_pass)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Superuser created: {admin_user}'))
            else:
                if not user.is_staff or not user.is_superuser:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save(update_fields=['is_staff', 'is_superuser'])
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Upgraded {admin_user} to superuser/staff'))
                self.stdout.write(f'  · Superuser {admin_user} ready')

            # Also grant staff/superuser to 'sreyas' if the account was registered on Render
            sreyas_user = User.objects.filter(username='sreyas').first()
            if sreyas_user and (not sreyas_user.is_staff or not sreyas_user.is_superuser):
                sreyas_user.is_staff = True
                sreyas_user.is_superuser = True
                sreyas_user.save(update_fields=['is_staff', 'is_superuser'])
                self.stdout.write(self.style.SUCCESS('  ✓ Granted admin/staff access to user: sreyas'))
        else:
            self.stdout.write(
                self.style.WARNING(
                    '  ! Production environment detected (DEBUG=False): skipping default "admin" account creation.\n'
                    '    Set ADMIN_USERNAME/ADMIN_PASSWORD or run on Render to auto-create.'
                )
            )

        # --- Categories ---
        cats = [
            {'name': 'Smartphones', 'description': 'The latest flagship and mid-range smartphones.', 'sort_order': 1, 'image': 'categories/cat_smartphones.svg'},
            {'name': 'Laptops', 'description': 'Powerful laptops for work, creativity, and gaming.', 'sort_order': 2, 'image': 'categories/cat_laptops.svg'},
            {'name': 'Audio', 'description': 'Headphones, earbuds and premium speakers.', 'sort_order': 3, 'image': 'categories/cat_audio.svg'},
            {'name': 'Wearables', 'description': 'Smart watches and fitness trackers.', 'sort_order': 4, 'image': 'categories/cat_wearables.svg'},
            {'name': 'Tablets', 'description': 'Versatile tablets for creation and entertainment.', 'sort_order': 5, 'image': 'categories/cat_tablets.svg'},
            {'name': 'Accessories', 'description': 'Cases, chargers, cables and more.', 'sort_order': 6, 'image': 'categories/cat_accessories.svg'},
        ]
        cat_objs = {}
        for c in cats:
            name = c['name']
            slug = slugify(name)
            obj = Category.objects.filter(name=name).first() or Category.objects.filter(slug=slug).first()
            if not obj:
                obj = Category.objects.create(**c)
                self.stdout.write(f"  ✓ Category created: {name}")
            else:
                # Safe: do not overwrite user-customized category data, only attach image if empty
                if not obj.image and c.get('image'):
                    obj.image = c['image']
                    obj.save(update_fields=['image'])
                self.stdout.write(f"  · Category preserved: {name}")
            cat_objs[name] = obj

        # --- Products ---
        products = [
            # Smartphones
            {'name': 'Luminex Pro 15', 'category': 'Smartphones',
             'short_description': 'Our most advanced smartphone with a triple-camera system and all-day battery.',
             'description': 'The Luminex Pro 15 features a stunning 6.7" OLED display with ProMotion technology, the fastest chip ever in a smartphone, and a revolutionary triple-camera system with 48MP main sensor. Experience photography like never before.',
             'price': 129900, 'original_price': 149900, 'stock': 50, 'is_featured': True, 'is_new_arrival': True,
             'main_image': 'products/luminex_pro_15.svg'},
            {'name': 'Luminex Air 15', 'category': 'Smartphones',
             'short_description': 'Slim, powerful and beautiful. The perfect everyday smartphone.',
             'description': 'The Luminex Air 15 brings the best of Luminex technology in a lighter, more affordable package. 6.1" OLED display, dual cameras, and incredible performance.',
             'price': 79900, 'original_price': None, 'stock': 120, 'is_featured': True,
             'main_image': 'products/luminex_air_15.svg'},
            {'name': 'Luminex Mini 15', 'category': 'Smartphones',
             'short_description': 'Big power in a compact design.',
             'description': 'Don\'t let its size fool you. The Luminex Mini packs a powerful punch with the same chip as the Pro, in a palm-friendly 5.4" design.',
             'price': 69900, 'original_price': 74900, 'stock': 80,
             'main_image': 'products/luminex_mini_15.svg'},

            # Laptops
            {'name': 'Luminex Book Pro 16', 'category': 'Laptops',
             'short_description': 'The ultimate laptop for professionals with a brilliant 16" Liquid Retina display.',
             'description': 'The Luminex Book Pro 16 is built for those who push limits. With the revolutionary Luminex M3 Pro chip, up to 22 hours of battery life, and an immersive 16.2" Liquid Retina XDR display, it\'s the most powerful laptop we\'ve ever made.',
             'price': 249900, 'original_price': 269900, 'stock': 30, 'is_featured': True, 'is_new_arrival': True,
             'main_image': 'products/luminex_book_pro_16.svg'},
            {'name': 'Luminex Book Air 15', 'category': 'Laptops',
             'short_description': 'Impossibly thin, remarkably capable.',
             'description': 'The Luminex Book Air is the world\'s best consumer laptop. Thin, light, fast, and with all-day battery life — it\'s everything you need in one incredibly thin design.',
             'price': 119900, 'original_price': None, 'stock': 60, 'is_featured': True,
             'main_image': 'products/luminex_book_air_15.svg'},

            # Audio
            {'name': 'Luminex Buds Pro 3', 'category': 'Audio',
             'short_description': 'Industry-leading noise cancellation with adaptive audio.',
             'description': 'Luminex Buds Pro feature industry-leading Active Noise Cancellation, Adaptive Audio that automatically adjusts to your environment, and Personalised Spatial Audio for an immersive listening experience.',
             'price': 24900, 'original_price': 26900, 'stock': 200, 'is_featured': True, 'is_new_arrival': True,
             'main_image': 'products/luminex_buds_pro_3.svg'},
            {'name': 'Luminex Phones Max', 'category': 'Audio',
             'short_description': 'Over-ear headphones with premium sound and 30-hour battery.',
             'description': 'The Luminex Phones Max deliver the ultimate headphone experience with high-fidelity audio, Active Noise Cancellation, and up to 30 hours of listening time.',
             'price': 59900, 'original_price': 64900, 'stock': 45,
             'main_image': 'products/luminex_phones_max.svg'},

            # Wearables
            {'name': 'Luminex Watch Ultra 2', 'category': 'Wearables',
             'short_description': 'The most rugged and capable Luminex Watch ever built.',
             'description': 'Luminex Watch Ultra 2 is designed for athletes, adventurers, and explorers. With precision dual-frequency GPS, up to 60 hours of battery, and a 49mm titanium case, it goes where you go.',
             'price': 89900, 'original_price': 94900, 'stock': 25, 'is_new_arrival': True,
             'main_image': 'products/luminex_watch_ultra_2.svg'},
            {'name': 'Luminex Watch Series 9', 'category': 'Wearables',
             'short_description': 'Smarter, brighter, more personal than ever.',
             'description': 'Luminex Watch Series 9 features a brighter display, the new S9 chip, and powerful health capabilities including Blood Oxygen measurement, ECG, and crash detection.',
             'price': 41900, 'original_price': None, 'stock': 90, 'is_featured': True,
             'main_image': 'products/luminex_watch_series_9.svg'},

            # Tablets
            {'name': 'Luminex Pad Pro 13"', 'category': 'Tablets',
             'short_description': 'The most advanced display. The most powerful chip. The thinnest design.',
             'description': 'The Luminex Pad Pro with the Ultra Retina XDR display features an astonishingly thin 5.1mm design and the groundbreaking Luminex M4 chip.',
             'price': 109900, 'original_price': 119900, 'stock': 35, 'is_new_arrival': True,
             'main_image': 'products/luminex_pad_pro_13.svg'},

            # Accessories
            {'name': 'Luminex MagCharge 30W', 'category': 'Accessories',
             'short_description': 'Fast wireless charging for your Luminex devices.',
             'description': 'The Luminex MagCharge delivers up to 30W of wireless power to your Luminex devices through MagSafe-compatible magnets for perfectly aligned charging.',
             'price': 3900, 'original_price': 4900, 'stock': 500,
             'main_image': 'products/luminex_magcharge.svg'},
            {'name': 'Luminex Smart Folio', 'category': 'Accessories',
             'short_description': 'Protective case with Smart Connector for Luminex Pad Pro.',
             'description': 'The Luminex Smart Folio is made from durable, soft-touch material and features the Smart Connector for automatic power and data transfer. Protects your Luminex Pad Pro front and back.',
             'price': 6900, 'original_price': None, 'stock': 150,
             'main_image': 'products/luminex_smart_folio.svg'},
        ]

        for p in products:
            cat_name = p.pop('category')
            cat = cat_objs.get(cat_name)
            name = p['name']
            slug = slugify(name)
            prod = Product.objects.filter(name=name).first() or Product.objects.filter(slug=slug).first()
            if not prod:
                prod = Product.objects.create(**p, category=cat)
                self.stdout.write(f"  ✓ Product created: {prod.name}")
            else:
                # Safe: preserve all existing pricing, stock, description, and status
                if not prod.main_image and p.get('main_image'):
                    prod.main_image = p['main_image']
                    prod.save(update_fields=['main_image'])
                self.stdout.write(f"  · Product preserved: {prod.name}")

        # --- Banners ---
        # Ensure unwanted Luminex Book Pro 16 hero banner is removed from database if present
        Banner.objects.filter(title='Luminex Book Pro 16', position='hero').delete()

        banners = [
            {
                'title': 'Luminex Pro 15',
                'subtitle': 'Forged in Innovation',
                'description': 'The most powerful smartphone ever created. Experience the future, today.',
                'cta_text': 'Learn More',
                'cta_link': '/products/?category=smartphones',
                'image': 'products/luminex_pro_15.svg',
                'bg_color': '#1d1d1f',
                'text_color': '#f5f5f7',
                'position': 'hero',
                'sort_order': 0,
            },
            {
                'title': 'Buds Pro 3',
                'subtitle': 'Hear Everything. Block Out the Rest.',
                'description': 'Industry-leading noise cancellation meets studio-quality sound.',
                'cta_text': 'Shop Audio',
                'cta_link': '/category/audio/',
                'bg_color': '#0071e3',
                'text_color': '#ffffff',
                'position': 'promo',
                'sort_order': 0,
            },
            {
                'title': 'Watch Ultra 2',
                'subtitle': 'Beyond Limits',
                'description': 'Built for the most extreme athletes and adventures on the planet.',
                'cta_text': 'Explore Wearables',
                'cta_link': '/category/wearables/',
                'bg_color': '#1c1c1e',
                'text_color': '#ffffff',
                'position': 'promo',
                'sort_order': 1,
            },
        ]

        for b in banners:
            title = b['title']
            pos = b['position']
            banner = Banner.objects.filter(title=title, position=pos).first()
            if not banner:
                banner = Banner.objects.create(**b)
                self.stdout.write(f"  ✓ Banner created: {banner.title} ({pos})")
            else:
                if not banner.image and b.get('image'):
                    banner.image = b['image']
                    banner.save(update_fields=['image'])
                self.stdout.write(f"  · Banner preserved: {banner.title} ({pos})")

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data seeded successfully!'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Login: admin / admin123')
