"""
The Unit-Test/Code Cycle:

In the terminal, run the unit tests and see how they fail.

In the editor, make a minimal code change to address the current test failure.

Repeat!
"""

from django.urls import resolve
from django.test import TestCase
# from django.http import HttpRequest

from fridge.views import home_page


class HomePageTest(TestCase):

    """ Old test
    def test_root_url_resolves_to_home_page_view(self):
        # find what view function url should map to
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    """

    def test_uses_home_template(self):
        # Instead of manually creating an HttpRequest object
        # and calling the view function directly,
        # call self.client.get, passing it the URL to test.
        response = self.client.get('/')
        """ Old method using HttpRequest
        # HttpRequest object is what Django sees when a user’s browser asks
        # for a page
        request = HttpRequest()
        # pass it to a view, which gives a response - instance of HttpResponse
        response = home_page(request)
        """
        # convert raw bytes to html
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Ask Fridge</title>', html)
        self.assertTemplateUsed(response, 'home.html')
