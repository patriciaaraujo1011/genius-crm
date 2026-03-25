from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from crm.models import Funnel, FunnelPage, OrderBump, Product


class FunnelViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(  # nosec: test fixture
            username="testuser", password="testpass123"
        )
        cls.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="Test description",
            price=99.99,
        )
        cls.funnel = Funnel.objects.create(
            name="Test Funnel",
            slug="test-funnel",
            is_active=True,
        )
        cls.landing_page = FunnelPage.objects.create(
            funnel=cls.funnel,
            page_type="landing",
            title="Test Landing",
            order=1,
        )
        cls.order_page = FunnelPage.objects.create(
            funnel=cls.funnel,
            page_type="order",
            title="Test Order",
            order=2,
        )
        cls.upsell_page = FunnelPage.objects.create(
            funnel=cls.funnel,
            page_type="upsell",
            title="Test Upsell",
            order=3,
        )
        cls.thankyou_page = FunnelPage.objects.create(
            funnel=cls.funnel,
            page_type="thank_you",
            title="Test Thank You",
            order=4,
        )
        cls.order_bump = OrderBump.objects.create(
            funnel=cls.funnel,
            product=cls.product,
            headline="Test Order Bump",
            is_active=True,
        )

    def setUp(self):
        self.client = Client()

    def test_landing_page_loads(self):
        response = self.client.get(
            reverse("funnel_landing", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 200)

    def test_order_page_loads(self):
        response = self.client.get(
            reverse("funnel_order", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 200)

    def test_checkout_requires_post(self):
        response = self.client.get(
            reverse("funnel_checkout", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 405)

    def test_upsell_page_loads(self):
        response = self.client.get(
            reverse("funnel_upsell", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 200)

    def test_thankyou_page_loads(self):
        response = self.client.get(
            reverse("funnel_thankyou", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 200)

    def test_offer_expired_page_loads(self):
        response = self.client.get(reverse("offer_expired"))
        self.assertEqual(response.status_code, 200)

    def test_inactive_funnel_returns_404(self):
        self.funnel.is_active = False
        self.funnel.save()
        response = self.client.get(
            reverse("funnel_landing", kwargs={"slug": "test-funnel"})
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_funnel_returns_404(self):
        response = self.client.get(
            reverse("funnel_landing", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)
