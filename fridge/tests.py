"""
The Unit-Test/Code Cycle:

In the terminal, run the unit tests and see how they fail.

In the editor, make a minimal code change to address the current test failure.

Repeat!

Triangulation
The unit-test/code cycle: Red, Green, Refactor:

Start by writing a unit test which fails (Red).

Write the simplest possible code to get it
to pass (Green), even if that means cheating.

Refactor to get to better code that makes more sense.

What justifies moving from an implementation where
we "cheat" to one we’re happy with?

One methodology is eliminate duplication:

if your test uses a magic constant (like the "1:"
in front of our list item), and your application code
also uses it, that counts as duplication,
so it justifies refactoring.
Removing the magic constant from the application code
usually means you have to stop cheating.

If that leaves things a little too vague, use
a second technique, which is called triangulation:
if your tests let you get away with writing "cheating"
code that you’re not happy with, like returning
a magic constant, write another test that forces you
to write some better code.
That’s what we’re doing when we extend the FT
to check that we get a "2:" when inputting
a second list item.

Refactoring:
Improve the code without changing its functionality
When refactoring, work on either the code or the tests,
but not both at once.
Test before refactoring.
Commit after refactoring.

Three Strikes and Refactor
- applies Don’t Repeat Yourself (DRY):

Code smell in FT: Three almost identical code blocks
doing the same thing.
You can copy and paste code once,
and it may be premature to try to remove the duplication
it causes, but once you get three occurrences,
it’s time to remove duplication.

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

    def test_can_save_a_POST_request(self):
        """To do a POST, call self.client.post.
        It takes a data argument which contains
        the form data we want to send. Then check that
        the text from our POST request ends up in
        the rendered HTML.
        """
        response = self.client.post('/',
                                    data={'item_text': 'A new list item'})
        self.assertIn('A new list item',
                      response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
