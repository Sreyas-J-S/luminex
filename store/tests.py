"""
Store app tests — views, models, and context processors.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Banner, Order, OrderItem, Cart, CartItem


class CategoryModelTest(TestCase):
    def test_slug_auto_generated(self):
        cat = Category.objects.create(name="Smartphones")
        self.assertEqual(cat.slug, "smartphones")

    def test_str(self):
        cat = Category.objects.create(name="Laptops")
        self.assertEqual(str(cat), "Laptops")


class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Test Category")

    def test_slug_auto_generated(self):
        p = Product.objects.create(
            name="Test Phone", category=self.cat,
            description="desc", price=9999, stock=10
        )
        self.assertEqual(p.slug, "test-phone")

    def test_sku_auto_generated(self):
        p = Product.objects.create(
            name="Test Laptop", category=self.cat,
            description="desc", price=49999, stock=5
        )
        self.assertTrue(p.sku.startswith("LMX-"))

    def test_discount_percent(self):
        p = Product.objects.create(
            name="Discounted Item", category=self.cat,
            description="desc", price=8000, original_price=10000, stock=1
        )
        self.assertEqual(p.discount_percent, 20)

    def test_in_stock(self):
        p = Product.objects.create(
            name="In Stock Item", category=self.cat,
            description="desc", price=1000, stock=5
        )
        self.assertTrue(p.in_stock)

    def test_out_of_stock(self):
        p = Product.objects.create(
            name="OOS Item", category=self.cat,
            description="desc", price=1000, stock=0
        )
        self.assertFalse(p.in_stock)


class HomeViewTest(TestCase):
    def test_homepage_200(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('store:home'))
        self.assertTemplateUsed(response, 'store/home.html')


class ProductListViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Audio")
        self.product = Product.objects.create(
            name="Test Earbuds", category=self.cat,
            description="Great earbuds", price=5999, stock=20,
            is_active=True
        )

    def test_product_list_200(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_shows_products(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertContains(response, "Test Earbuds")

    def test_search_returns_results(self):
        response = self.client.get(reverse('store:product_list') + '?q=earbuds')
        self.assertContains(response, "Test Earbuds")

    def test_search_no_results(self):
        response = self.client.get(reverse('store:product_list') + '?q=notexist')
        self.assertNotContains(response, "Test Earbuds")

    def test_inactive_products_hidden(self):
        Product.objects.create(
            name="Hidden Product", category=self.cat,
            description="hidden", price=100, stock=1, is_active=False
        )
        response = self.client.get(reverse('store:product_list'))
        self.assertNotContains(response, "Hidden Product")


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Wearables")
        self.product = Product.objects.create(
            name="Smart Watch", category=self.cat,
            description="A great watch", price=29999, stock=10, is_active=True
        )

    def test_product_detail_200(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_shows_name(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertContains(response, "Smart Watch")

    def test_inactive_product_404(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 404)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Tablets")

    def test_category_detail_200(self):
        response = self.client.get(reverse('store:category_detail', kwargs={'slug': self.cat.slug}))
        self.assertEqual(response.status_code, 200)

    def test_inactive_category_404(self):
        self.cat.is_active = False
        self.cat.save()
        response = self.client.get(reverse('store:category_detail', kwargs={'slug': self.cat.slug}))
        self.assertEqual(response.status_code, 404)


class CartAndCheckoutTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Smartphones")
        self.product = Product.objects.create(
            name="Luminex Pro 15", category=self.cat,
            description="Flagship", price=129900, stock=10, is_active=True
        )
        self.user = User.objects.create_user(
            username="buyer", email="buyer@example.com", password="password123",
            first_name="Jane", last_name="Doe"
        )

    def test_cart_detail_empty(self):
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Bag is empty.")

    def test_cart_add_product(self):
        response = self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        self.assertRedirects(response, reverse('store:cart_detail'))
        response = self.client.get(reverse('store:cart_detail'))
        self.assertContains(response, "Luminex Pro 15")
        self.assertContains(response, "₹259,800.00")

    def test_cart_stock_limit_enforced(self):
        # Request 15 when only 10 available
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 15}
        )
        response = self.client.get(reverse('store:cart_detail'))
        # Quantity should be capped at 10
        self.assertEqual(response.context['cart'].total_items, 10)

    def test_checkout_and_safe_stock_deduction(self):
        self.client.login(username="buyer", password="password123")
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 3}
        )

        checkout_data = {
            'full_name': 'Jane Doe',
            'email': 'buyer@example.com',
            'phone': '9876543210',
            'address_line1': '123 High Street',
            'address_line2': 'Apt 4B',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560001',
        }
        response = self.client.post(reverse('store:checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        # Product stock should be decremented from 10 to 7
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

        # Cart should now be empty
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.context['cart'].total_items, 0)

    def test_cart_update_and_remove(self):
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        cart_response = self.client.get(reverse('store:cart_detail'))
        cart_item = cart_response.context['cart_items'][0]

        # Update to 4
        self.client.post(
            reverse('store:cart_update', kwargs={'item_id': cart_item.id}),
            {'quantity': 4}
        )
        cart_response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(cart_response.context['cart'].total_items, 4)

        # Remove item
        self.client.post(reverse('store:cart_remove', kwargs={'item_id': cart_item.id}))
        cart_response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(cart_response.context['cart'].total_items, 0)


class OrderSecurityTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="alice", email="alice@example.com", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="bob", email="bob@example.com", password="password123"
        )
        self.staff_user = User.objects.create_superuser(
            username="adminuser", email="admin@example.com", password="password123"
        )
        self.auth_order = Order.objects.create(
            user=self.owner,
            full_name="Alice Smith",
            email="alice@example.com",
            phone="9876543210",
            address_line1="123 Apple St",
            city="Bengaluru",
            state="Karnataka",
            postal_code="560001",
            total_amount=129900,
            status="processing"
        )
        self.guest_order = Order.objects.create(
            user=None,
            full_name="Guest User",
            email="guest@example.com",
            phone="9123456789",
            address_line1="456 Guest Ave",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            total_amount=5999,
            status="processing"
        )

    def test_owner_can_view_own_order(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.auth_order.order_number})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.auth_order.order_number)

    def test_different_user_cannot_view_others_order(self):
        self.client.login(username="bob", password="password123")
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.auth_order.order_number})
        )
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_view_auth_order(self):
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.auth_order.order_number})
        )
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_view_unauthorized_guest_order(self):
        # A visitor who did not place this guest order should be rejected
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.guest_order.order_number})
        )
        self.assertEqual(response.status_code, 403)

    def test_guest_session_can_view_their_guest_order(self):
        # When a guest checks out, their session is authorized
        session = self.client.session
        session['guest_orders'] = [self.guest_order.order_number]
        session.save()

        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.guest_order.order_number})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guest_order.order_number)

    def test_staff_can_view_any_order(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': self.guest_order.order_number})
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_order_number_returns_404(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(
            reverse('store:order_confirmation', kwargs={'order_number': 'LMX-NONEXISTENT'})
        )
        self.assertEqual(response.status_code, 404)


class CartCalculationsAndDisplayTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Accessories")
        self.cheap_product = Product.objects.create(
            name="USB-C Cable", category=self.cat,
            description="Durable woven cable", price=1900, stock=50, is_active=True
        )
        self.expensive_product = Product.objects.create(
            name="Pro Display", category=self.cat,
            description="5K Retina", price=129900, stock=10, is_active=True
        )

    def test_cart_formatted_total_property(self):
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.cheap_product.id}),
            {'quantity': 2}
        )
        cart_response = self.client.get(reverse('store:cart_detail'))
        cart = cart_response.context['cart']
        self.assertEqual(cart.formatted_total, "₹3,800.00")

    def test_cart_under_free_shipping_threshold(self):
        # 1 unit of ₹1,900 is under ₹5,000 threshold
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.cheap_product.id}),
            {'quantity': 1}
        )
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['qualifies_free_shipping'])
        self.assertEqual(response.context['free_shipping_deficit'], 3100)
        self.assertEqual(response.context['delivery_fee'], 499)
        self.assertContains(response, "Add ₹3100.00 more to your bag to qualify for")

    def test_cart_qualifies_for_free_shipping(self):
        # 1 unit of ₹129,900 exceeds ₹5,000 threshold
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.expensive_product.id}),
            {'quantity': 1}
        )
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['qualifies_free_shipping'])
        self.assertEqual(response.context['free_shipping_deficit'], 0)
        self.assertEqual(response.context['delivery_fee'], 0)
        self.assertContains(response, "Free delivery on this order.")


class BannerDynamicRenderingTest(TestCase):
    def test_active_hero_banner_renders_on_homepage(self):
        banner = Banner.objects.create(
            title="Spring Launch Special",
            subtitle="New Season Arrival",
            position="hero",
            is_active=True,
            sort_order=0
        )
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spring Launch Special")
        self.assertContains(response, "New Season Arrival")

    def test_inactive_banner_does_not_render(self):
        banner = Banner.objects.create(
            title="Draft Secret Promotion",
            subtitle="Hidden Subtitle",
            position="hero",
            is_active=False
        )
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Draft Secret Promotion")


class CheckoutReliabilityTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Audio", slug="audio")
        self.product = Product.objects.create(
            name="Studio Headphones",
            slug="studio-headphones",
            category=self.category,
            price=9999,
            stock=5,
            is_active=True
        )
        self.checkout_data = {
            'full_name': 'Dev Tester',
            'email': 'dev@example.com',
            'phone': '9876543210',
            'address_line1': '101 Silicon Lane',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560100',
        }

    def test_checkout_nonce_rendered_in_form(self):
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 1}
        )
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="checkout_nonce"')
        self.assertContains(response, 'id="checkout-submit-btn"')
        self.assertContains(response, 'checkout-btn-spinner')

    def test_repeated_checkout_submission_idempotency(self):
        # Add 1 item to cart
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 1}
        )
        # Fetch checkout page to initialize nonce in session
        get_resp = self.client.get(reverse('store:checkout'))
        nonce = get_resp.context['checkout_nonce']

        post_data = {**self.checkout_data, 'checkout_nonce': nonce}

        # First checkout submission
        resp1 = self.client.post(reverse('store:checkout'), post_data)
        self.assertEqual(resp1.status_code, 302)
        order = Order.objects.get(email='dev@example.com')
        self.assertEqual(resp1.url, reverse('store:order_confirmation', kwargs={'order_number': order.order_number}))

        # Verify stock and order count
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)
        self.assertEqual(Order.objects.count(), 1)

        # Second repeated checkout submission (e.g. rapid double click / replay with same nonce)
        resp2 = self.client.post(reverse('store:checkout'), post_data)
        self.assertEqual(resp2.status_code, 302)
        # Must redirect safely to the SAME order confirmation
        self.assertEqual(resp2.url, reverse('store:order_confirmation', kwargs={'order_number': order.order_number}))

        # Verify no duplicate order was created and stock was not decremented twice
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)

    def test_failed_checkout_form_preserves_stock_and_cart(self):
        # Add item to bag
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        initial_stock = self.product.stock
        # Submit invalid checkout (missing required fields)
        response = self.client.post(reverse('store:checkout'), {'full_name': 'Incomplete User'})
        self.assertEqual(response.status_code, 200)

        # Stock must not be touched
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock)

        # Bag must still contain items
        bag_resp = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(bag_resp.context['cart'].total_items, 2)

    def test_failed_transaction_rolls_back_stock_and_cart(self):
        from unittest.mock import patch
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        initial_stock = self.product.stock

        get_resp = self.client.get(reverse('store:checkout'))
        nonce = get_resp.context['checkout_nonce']

        # Simulate unexpected DB failure inside atomic block during OrderItem creation
        with patch('store.models.OrderItem.objects.create', side_effect=RuntimeError("Simulated DB write failure")):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('store:checkout'), {**self.checkout_data, 'checkout_nonce': nonce})

        # Product stock must remain unchanged
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock)

        # No order should have persisted
        self.assertEqual(Order.objects.count(), 0)

        # Cart items must still exist
        bag_resp = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(bag_resp.context['cart'].total_items, 2)


class SeedDemoSecurityTest(TestCase):
    def test_seed_demo_in_production_skips_insecure_default_superuser(self):
        from django.core.management import call_command
        from io import StringIO
        from django.test import override_settings

        out = StringIO()
        with override_settings(DEBUG=False):
            call_command('seed_demo', stdout=out)

        output = out.getvalue()
        self.assertIn('skipping default "admin" account creation', output)
        self.assertFalse(User.objects.filter(username='admin').exists())


class ProductionSettingsValidationTest(TestCase):
    def test_production_settings_raises_if_secret_key_missing(self):
        import importlib
        from unittest.mock import patch
        from django.core.exceptions import ImproperlyConfigured

        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                import luminex.settings.production
                importlib.reload(luminex.settings.production)
            self.assertIn("SECRET_KEY", str(ctx.exception))

    def test_production_settings_raises_if_database_url_missing(self):
        import importlib
        from unittest.mock import patch
        from django.core.exceptions import ImproperlyConfigured

        mock_env = {
            'SECRET_KEY': '1234567890123456789012345678901234567890',
            'ALLOWED_HOSTS': 'test.onrender.com',
            'CSRF_TRUSTED_ORIGINS': 'https://test.onrender.com',
        }
        with patch.dict('os.environ', mock_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                import luminex.settings.production
                importlib.reload(luminex.settings.production)
            self.assertIn("DATABASE_URL", str(ctx.exception))

    def test_production_settings_raises_if_s3_keys_missing_when_bucket_specified(self):
        import importlib
        from unittest.mock import patch
        from django.core.exceptions import ImproperlyConfigured

        mock_env = {
            'SECRET_KEY': '1234567890123456789012345678901234567890',
            'ALLOWED_HOSTS': 'test.onrender.com',
            'CSRF_TRUSTED_ORIGINS': 'https://test.onrender.com',
            'DATABASE_URL': 'sqlite:///mock_test.sqlite3',
            'AWS_STORAGE_BUCKET_NAME': 'my-bucket',
        }
        with patch.dict('os.environ', mock_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                import luminex.settings.production
                importlib.reload(luminex.settings.production)
            self.assertIn("AWS_ACCESS_KEY_ID", str(ctx.exception))

    def test_production_settings_valid_configuration(self):
        import importlib
        from unittest.mock import patch

        mock_env = {
            'SECRET_KEY': '1234567890123456789012345678901234567890',
            'ALLOWED_HOSTS': 'test.onrender.com',
            'CSRF_TRUSTED_ORIGINS': 'https://test.onrender.com',
            'DATABASE_URL': 'sqlite:///mock_test.sqlite3',
            'ALLOW_EPHEMERAL_MEDIA': 'True',
        }
        with patch.dict('os.environ', mock_env, clear=True):
            import luminex.settings.production
            mod = importlib.reload(luminex.settings.production)
            self.assertFalse(mod.DEBUG)
            self.assertEqual(mod.ALLOWED_HOSTS, ['test.onrender.com'])
            self.assertTrue(mod.SECURE_SSL_REDIRECT)
            self.assertTrue(mod.SESSION_COOKIE_SECURE)
            self.assertTrue(mod.CSRF_COOKIE_SECURE)


