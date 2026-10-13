"""
Store app tests — views, models, and context processors.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Banner


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


