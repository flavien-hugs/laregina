# pages.tests.tests_models.py

from django.urls import reverse
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch

from pages.models import Contact, Testimonial, Promotion


class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(
        	full_name='flavien hugs',
        	email='flavienhugs@pm.me',
        	phone='+2250151571396',
        	subject='demande de partenariat',
        	company='Unsta INC',
        	message='je souhaite uns partenariat.',
        )

    def test_contact_url(self):
        try:
            url = reverse('pages:contact')
        except NoReverseMatch:
            assert False
        response = self.client.get(url)
        assert response.status_code == 200


class TestimonialtTestCase(TestCase):
    def setUp(self):
        Testimonial.objects.create(
            full_name='flavien hugs',
            status_client='Unsta INC',
            message='je souhaite uns partenariat.',
            image='',
        )
