from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from pages.models import Contact
from pages.models import Testimonial


class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(
            full_name="flavien hugs",
            email="flavienhugs@pm.me",
            phone="+2250151571396",
            subject="demande de partenariat",
            company="Unsta INC",
            message="je souhaite uns partenariat.",
        )

    def test_contact_url(self):
        try:
            url = reverse("pages:contact")
        except NoReverseMatch as err:
            raise AssertionError("Reverse for 'pages:contact' not found.") from err
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestimonialtTestCase(TestCase):
    def setUp(self):
        Testimonial.objects.create(
            full_name="flavien hugs",
            status_client="Unsta INC",
            message="je souhaite uns partenariat.",
            image="",
        )
