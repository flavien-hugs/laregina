# search.tests.test_views.py

import httplib
from django.utils import html
from django.urls import reverse
from django.test import TestCase, Client


class SearchTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        home_url = reverse('catalogue:product_list')
        response = self.client.get(home_url)
        self.failUnless(response.status_code, httplib.OK)


    def test_html_escaped(self):
        """
            le texte de recherche affiché sur
            la page de résultats est codé en HTML
        """
        search_term = '<script>alert(xss)</script>'
        search_url = reverse('search')
        search_request = search_url + '?q=' + search_term
        response = self.client.get(search_request)
        self.failUnlessEqual(response.status_code, httplib.OK)
        escaped_term = html.escape(search_term)
        self.assertContains(response, escaped_term)
