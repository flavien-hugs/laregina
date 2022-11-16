# catalogue.tests.test_views.py


from django.urls import reverse
from django.test import TestCase, TransactionTestCase
from django.http import HttpRequest


class HomePageTestCase(TransactionTestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_home_page_contains_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, "")

    def test_home_page_does_not_contains_incorrect_html(self):
        response = self.client.get("/")
        self.assertNotContains(response, "Hi there! No data found.")


class AboutPageTestCase(TransactionTestCase):
    def test_about_page_status_code(self):
        response = self.client.get("/about-us/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("about-us"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("about-us"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about-us.html")

    def test_about_page_contains_correct_html(self):
        response = self.client.get("/about-us/")
        self.assertContains(response, "")

    def test_about_page_does_not_contains_incorrect_html(self):
        response = self.client.get("/about-us/")
        self.assertNotContains(response, "Hi there! No data found.")


class FaqsPageTestCase(TransactionTestCase):
    def test_faqs_page_status_code(self):
        response = self.client.get("/faqs/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("faqs"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("faqs"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/faqs.html")

    def test_faqs_page_contains_correct_html(self):
        response = self.client.get("/faqs/")
        self.assertContains(response, "")

    def test_faqs_page_does_not_contain_incorrect_html(self):
        response = self.client.get("/faqs/")
        self.assertNotContains(response, "Hi there! No data found.")


class TrackingOrderPageTestCase(TransactionTestCase):
    def test_tracking_order_page_status_code(self):
        response = self.client.get("/tracking-order/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("tracking-order"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("tracking-order"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/tracking-order.html")

    def test_tracking_order_page_contains_correct_html(self):
        response = self.client.get("/tracking-order/")
        self.assertContains(response, "")

    def test_tracking_order_page_does_not_contain_incorrect_html(self):
        response = self.client.get("/tracking-order/")
        self.assertNotContains(response, "Hi there! No data found.")
