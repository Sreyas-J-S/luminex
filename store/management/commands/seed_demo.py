"""
Management command to seed demo data for Luminex store.
Run: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, Banner


class Command(BaseCommand):
    help = 'Seeds the database with demo categories, products, and banners'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Luminex demo data...')

        # --- Superuser ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@luminex.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('  ✓ Superuser created: admin / admin123'))
        else:
            self.stdout.write('  · Superuser already exists')

        # --- Categories ---
        cats = [
            {'name': 'Smartphones', 'description': 'The latest flagship and mid-range smartphones.', 'sort_order': 1},
            {'name': 'Laptops', 'description': 'Powerful laptops for work, creativity, and gaming.', 'sort_order': 2},
            {'name': 'Audio', 'description': 'Headphones, earbuds and premium speakers.', 'sort_order': 3},
            {'name': 'Wearables', 'description': 'Smart watches and fitness trackers.', 'sort_order': 4},
            {'name': 'Tablets', 'description': 'Versatile tablets for creation and entertainment.', 'sort_order': 5},
            {'name': 'Accessories', 'description': 'Cases, chargers, cables and more.', 'sort_order': 6},
        ]
        cat_objs = {}
        for c in cats:
            obj, created = Category.objects.get_or_create(name=c['name'], defaults=c)
            cat_objs[c['name']] = obj
            if created:
                self.stdout.write(f"  ✓ Category: {c['name']}")

        # --- Products ---
        products = [
            # Smartphones
            {'name': 'Luminex Pro 15', 'category': 'Smartphones',
             'short_description': 'Our most advanced smartphone with a triple-camera system and all-day battery.',
             'description': 'The Luminex Pro 15 features a stunning 6.7" OLED display with ProMotion technology, the fastest chip ever in a smartphone, and a revolutionary triple-camera system with 48MP main sensor. Experience photography like never before.',
             'price': 129900, 'original_price': 149900, 'stock': 50, 'is_featured': True, 'is_new_arrival': True},
            {'name': 'Luminex Air 15', 'category': 'Smartphones',
             'short_description': 'Slim, powerful and beautiful. The perfect everyday smartphone.',
             'description': 'The Luminex Air 15 brings the best of Luminex technology in a lighter, more affordable package. 6.1" OLED display, dual cameras, and incredible performance.',
             'price': 79900, 'original_price': None, 'stock': 120, 'is_featured': True},
            {'name': 'Luminex Mini 15', 'category': 'Smartphones',
             'short_description': 'Big power in a compact design.',
             'description': 'Don\'t let its size fool you. The Luminex Mini packs a powerful punch with the same chip as the Pro, in a palm-friendly 5.4" design.',
             'price': 69900, 'original_price': 74900, 'stock': 80},

            # Laptops
            {'name': 'Luminex Book Pro 16', 'category': 'Laptops',
             'short_description': 'The ultimate laptop for professionals with a brilliant 16" Liquid Retina display.',
             'description': 'The Luminex Book Pro 16 is built for those who push limits. With the revolutionary Luminex M3 Pro chip, up to 22 hours of battery life, and an immersive 16.2" Liquid Retina XDR display, it\'s the most powerful laptop we\'ve ever made.',
             'price': 249900, 'original_price': 269900, 'stock': 30, 'is_featured': True, 'is_new_arrival': True},
            {'name': 'Luminex Book Air 15', 'category': 'Laptops',
             'short_description': 'Impossibly thin, remarkably capable.',
             'description': 'The Luminex Book Air is the world\'s best consumer laptop. Thin, light, fast, and with all-day battery life — it\'s everything you need in one incredibly thin design.',
             'price': 119900, 'original_price': None, 'stock': 60, 'is_featured': True},

            # Audio
            {'name': 'Luminex Buds Pro 3', 'category': 'Audio',
             'short_description': 'Industry-leading noise cancellation with adaptive audio.',
             'description': 'Luminex Buds Pro feature industry-leading Active Noise Cancellation, Adaptive Audio that automatically adjusts to your environment, and Personalised Spatial Audio for an immersive listening experience.',
             'price': 24900, 'original_price': 26900, 'stock': 200, 'is_featured': True, 'is_new_arrival': True},
            {'name': 'Luminex Phones Max', 'category': 'Audio',
             'short_description': 'Over-ear headphones with premium sound and 30-hour battery.',
             'description': 'The Luminex Phones Max deliver the ultimate headphone experience with high-fidelity audio, Active Noise Cancellation, and up to 30 hours of listening time.',
             'price': 59900, 'original_price': 64900, 'stock': 45},

            # Wearables
            {'name': 'Luminex Watch Ultra 2', 'category': 'Wearables',
             'short_description': 'The most rugged and capable Luminex Watch ever built.',
             'description': 'Luminex Watch Ultra 2 is designed for athletes, adventurers, and explorers. With precision dual-frequency GPS, up to 60 hours of battery, and a 49mm titanium case, it goes where you go.',
             'price': 89900, 'original_price': 94900, 'stock': 25, 'is_new_arrival': True},
            {'name': 'Luminex Watch Series 9', 'category': 'Wearables',
             'short_description': 'Smarter, brighter, more personal than ever.',
             'description': 'Luminex Watch Series 9 features a brighter display, the new S9 chip, and powerful health capabilities including Blood Oxygen measurement, ECG, and crash detection.',
             'price': 41900, 'original_price': None, 'stock': 90, 'is_featured': True},

            # Tablets
            {'name': 'Luminex Pad Pro 13"', 'category': 'Tablets',
             'short_description': 'The most advanced display. The most powerful chip. The thinnest design.',
             'description': 'The Luminex Pad Pro with the Ultra Retina XDR display features an astonishingly thin 5.1mm design and the groundbreaking Luminex M4 chip.',
             'price': 109900, 'original_price': 119900, 'stock': 35, 'is_new_arrival': True},

            # Accessories
            {'name': 'Luminex MagCharge 30W', 'category': 'Accessories',
             'short_description': 'Fast wireless charging for your Luminex devices.',
             'description': 'The Luminex MagCharge delivers up to 30W of wireless power to your Luminex devices through MagSafe-compatible magnets for perfectly aligned charging.',
             'price': 3900, 'original_price': 4900, 'stock': 500},
            {'name': 'Luminex Smart Folio', 'category': 'Accessories',
             'short_description': 'Protective case with Smart Connector for Luminex Pad Pro.',
             'description': 'The Luminex Smart Folio is made from durable, soft-touch material and features the Smart Connector for automatic power and data transfer. Protects your Luminex Pad Pro front and back.',
             'price': 6900, 'original_price': None, 'stock': 150},
        ]

        for p in products:
            cat = cat_objs.get(p.pop('category'))
            obj, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={**p, 'category': cat}
            )
            if created:
                self.stdout.write(f"  ✓ Product: {obj.name}")

        # --- Banners ---
        banners = [
            {
                'title': 'Luminex Pro 15',
                'subtitle': 'Forged in Innovation',
                'description': 'The most powerful smartphone ever created. Experience the future, today.',
                'cta_text': 'Learn More',
                'cta_link': '/products/?category=smartphones',
                'bg_color': '#1d1d1f',
                'text_color': '#f5f5f7',
                'position': 'hero',
                'sort_order': 0,
            },
            {
                'title': 'Luminex Book Pro 16',
                'subtitle': 'Built for Greatness',
                'description': 'Unstoppable performance. Unmatched battery. The professional laptop redefined.',
                'cta_text': 'Buy Now',
                'cta_link': '/products/?category=laptops',
                'bg_color': '#f5f5f7',
                'text_color': '#1d1d1f',
                'position': 'hero',
                'sort_order': 1,
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
            obj, created = Banner.objects.get_or_create(title=b['title'], defaults=b)
            if created:
                self.stdout.write(f"  ✓ Banner: {obj.title}")

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data seeded successfully!'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Login: admin / admin123')
