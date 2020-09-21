from django.urls import resolve
from django.test import TestCase
from fridge.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # find what view function url should map to
        found = resolve('/')
        self.assertEqual(found.func, home_page)
