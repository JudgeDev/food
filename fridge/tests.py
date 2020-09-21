from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from fridge.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # find what view function url should map to
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # HttpRequest object is what Django sees when a user’s browser asks
        # for a page
        request = HttpRequest()
        # pass it to a view, which gives a response - instance of HttpResponse
        response = home_page(request)
        # convert raw bytes to html
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Ask Fridge</title>', html)
        self.assertTrue(html.endswith('</html>'))
